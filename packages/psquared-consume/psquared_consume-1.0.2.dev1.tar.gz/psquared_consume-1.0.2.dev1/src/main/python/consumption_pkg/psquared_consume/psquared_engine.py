"""
Provide utilities to run the PSqaured state machine
"""

from typing import List, Tuple, Optional

import io
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import requests

from .execution_request import ExecutionRequest
from . import mock_server
from . import utils

HEADERS = {"Content-Type": "application/xml", "Accept": "application/xml"}
DEBUG = False
RESUBMISSION_LIMIT = 8

EXAMPLE_HTTP = "http://example.com/"
EXAMPLE_HTTPS = "https://example.com/"
EXAMPLE_URIS = (EXAMPLE_HTTP, EXAMPLE_HTTPS)


class RestfulFailure(Exception):
    """
    Thrown when a RESTful call does not complete as expected.
    """

    def __init__(self, message: str, error_code: int):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
        self.code = error_code


def _check_status(uri: str, response: requests.Response, expected: int) -> None:
    """
    Checks that the returned status code matches the expected one.

    Args:
        uri: The URI to which the request was made.
        response: the response to the request.
        expected: the expected status code.
    """
    if 400 == response.status_code:
        raise RestfulFailure(
            'Application at "' + uri + '" requires SSL certificate',
            response.status_code,
        )
    if 401 == response.status_code:
        raise RestfulFailure(
            'Not authorized to execute commands for Application at "' + uri,
            response.status_code,
        )
    if 404 == response.status_code:
        raise RestfulFailure(
            'Application at "' + uri + '" not found', response.status_code
        )
    if expected != response.status_code:
        raise RestfulFailure(
            f'Unexpected status ({str(response.status_code)}) returned from "{uri}"',
            response.status_code,
        )


def _get_valid_element(uri: str, element: ET.Element, tag: str) -> ET.Element:
    """
    Returns the valid tag element within the supplied element.

    Raises:
        RestfulFailure: When the supplied element does not contain
                the tag element.
    """
    tag_element = element.find(tag)
    if None is tag_element:
        raise RestfulFailure(
            f'Incomplete response returned from "{uri}", "{tag}" element is missing from'
            + ' "{element.tag}" element',
            1,
        )
    return tag_element


def _get_valid_text(uri: str, element: ET.Element, tag: str) -> str:
    """
    Returns the valid, non-null, contents for the tag element within the supplied element.

    Raises:
        RestfulFailure: When the supplied element does not contain
                the tag element or the tag element is null.
    """
    tag_element = element.find(tag)
    if None is tag_element or None is tag_element.text:
        raise RestfulFailure(
            f'Incomplete response returned from "{uri}", "{tag}" element is missing from'
            + ' "{element.tag}" element, or is empty',
            1,
        )
    return tag_element.text


def _prepare_attachment(message: Optional[str] = None) -> ET.Element:
    """
    Returns the 'attachment' document that includes the supplied message, if any.
    """
    attachment = ET.Element("attachment")
    if None is not message:
        msg = ET.Element("message")
        msg.text = message
        attachment.append(msg)
    return attachment


def _process(
    cmd: str,
    params: List[str],
    cmd_out: Optional[io.TextIOWrapper],
    cmd_err: Optional[io.TextIOWrapper],
) -> Tuple[int, str]:
    """
    Processes the supplied command, return any message created by the command while
    it was executing.

    Args:
        cmd: The command to process.
        params: The parameter to use with the command.
        cmd_out: Where to write the stdout of the command.
        cmd_out: Where to write the stderr of the command.
    """

    args = []
    args.append(cmd)
    args.extend(params)
    file_descriptor, message_file = tempfile.mkstemp(text=True)
    cmd_env = os.environ.copy()
    cmd_env["PP_MESSAGE_FILE"] = message_file
    with subprocess.Popen(args, env=cmd_env, stdout=cmd_out, stderr=cmd_err) as proc:
        result = proc.wait()
    message = os.fdopen(file_descriptor, "r").read()
    os.remove(message_file)
    return result, message.strip()


class Engine:  # pylint: disable=too-few-public-methods
    """
    This class guides a ExecutionRequest though the PSquared state machine.
    """

    def __init__(
        self,
        debug: Optional[bool] = None,
        cert: Optional[str] = None,
        key: Optional[str] = None,
        cacert: Optional[str] = None,
    ):
        """
        Creates an instance of this class.

        Args:
            cert: The path to the file holding this client's
                certificate.
            key: The path to the file holding this client's private
                key.
            cacert: The path to the known CA certificates.
        """
        self.__debug = debug
        self.__session = requests.Session()
        if (
            None is not cert
            and os.path.exists(cert)
            and None is not key
            and os.path.exists(key)
        ):
            self.__session.cert = (cert, key)
        if None is not cacert and os.path.exists(cacert):
            self.__session.verify = cacert
        self.__use_mock_server = False

    def __automatic_resubmission(self, uri: str, resubmission_count: int) -> str:
        """
        Resubmits this request as its previous engine failed top complete.

        Raise:
            ConnectionFailure: When the connection to the server can not be established.
        """
        if self.__use_mock_server:
            response = mock_server.get(uri)
        else:
            response = self.__session.get(uri)
        _check_status(uri, response, 200)
        if self.__debug:
            utils.pretty_print(uri, response.text)
        state = ET.fromstring(response.text)
        elements = state.findall("exits/exit")
        if 0 == len(elements):
            element = _get_valid_element(uri, state, "exited")
            name_text = _get_valid_text(uri, element, "name")
            if "reschedule" == name_text:
                uri_text = _get_valid_text(uri, element, "uri")
                return self.__get_execution_uri(uri_text, resubmission_count)
            raise RestfulFailure(
                "Another process has started processing this request, so this attempt will halt",
                409,
            )
        for exit_element in elements:
            name_text = _get_valid_text(uri, exit_element, "name")
            if "reschedule" == name_text:
                uri_text = _get_valid_text(uri, element, "uri")
                reschedule_uri = uri_text
                break

        state = self.__execute_transition(
            reschedule_uri, "Rescheduling as previous execution died"
        )
        elements = state.findall("exits/exit")
        if 0 == len(elements):
            raise RestfulFailure("Failed to correctly reschedule submission", 1)
        return self.__parse_submitted_response(uri, state, resubmission_count)

    def execute(  # pylint: disable=too-many-branches
        self, message_for_execute: str, request: ExecutionRequest, resubmission: bool
    ) -> None:
        """
        Executes an instance of the PSquared state machine.

        Args:
            request: the execution request to fulfill.
            message_for_execute: The message to associate with the
                "execute" transition.
        Raises:

        """

        if resubmission:
            resubmission_count = 0
        else:
            resubmission_count = -1
        executing_uri = self.__get_execution_uri(
            request.submission_uri, resubmission_count
        )
        processed_uri, failed_uri = self.__processing_beginning(
            executing_uri, message_for_execute
        )
        if None is request.arguments:
            params: List[str] = []
        else:
            params = request.arguments
        try:
            result, message = _process(
                request.cmd, params, request.cmd_out, request.cmd_err
            )
        except OSError as os_error:
            utils.eprint(request.cmd, params)
            utils.eprint("Failed to execute command")
            if None is not os_error.errno:
                utils.eprint("Error Number: " + str(os_error.errno))
            if None is not os_error.strerror:
                utils.eprint("Explanation: " + os_error.strerror)
            if None is not os_error.filename:
                utils.eprint("Filename: " + os_error.filename)
            result, message = (
                255,
                "Failed to execute command, check log file for details",
            )
        if 0 == result:
            self.__execute_transition(processed_uri, message)
            if None is not request.success_cmd:
                try:
                    _process(
                        request.success_cmd, params, request.cmd_out, request.cmd_err
                    )
                except OSError as exc:
                    raise RestfulFailure(
                        'Failed to execute "success" command', 255
                    ) from exc
        else:
            self.__execute_transition(failed_uri, message)
            if None is not request.failure_cmd:
                try:
                    _process(
                        request.failure_cmd, params, request.cmd_out, request.cmd_err
                    )
                except OSError as exc:
                    raise RestfulFailure(
                        'Failed to execute "failure" command', 255
                    ) from exc

    def __execute_transition(
        self, uri: str, message: Optional[str] = None
    ) -> ET.Element:
        """
        Requests the PSquared instance create a new realized state.

        Args:
            uri: The URI of the destination of the transition.
            message: The message, if any, to attach to the transition.

        Returns:
            The XML document that was the response to the request.

        Raise:
            RestfulFailure: If the status code of the response is not what was expected.
        """
        # Prepare attachment document
        attachment = _prepare_attachment(message)
        if self.__debug:
            utils.pretty_print(uri, str(ET.tostring(attachment), "utf-8"), False)
        if self.__use_mock_server:
            response = mock_server.post(uri)
        else:
            response = self.__session.post(
                uri, data=ET.tostring(attachment), headers=HEADERS
            )
        if 404 == response.status_code:
            raise RestfulFailure(
                f'Exit request "{uri}" not found', response.status_code
            )
        if 409 == response.status_code:
            raise RestfulFailure(
                "Another process has changed the processing of this request, so this attempt will"
                + " halt",
                response.status_code,
            )
        if 201 == response.status_code:
            if self.__debug:
                utils.pretty_print(uri, response.text)
            return ET.fromstring(response.text)
        raise RestfulFailure(
            f'Unexpected status ({str(response.status_code)}) returned from "{uri}"',
            response.status_code,
        )

    def __get_execution_uri(self, uri: str, resubmission_count: int) -> str:
        """
        Returns the URI that will signal to PSqaured that processing has begun.

        Args:
            uri: The URL associated with the submission of execution request.

        Raises:
            ConnectionFailure: When the connection to the server can not be established.
        """
        if uri.startswith(EXAMPLE_URIS):
            self.__use_mock_server = True
            response = mock_server.get(uri)
        else:
            response = self.__session.get(uri)
        _check_status(uri, response, 200)
        if self.__debug:
            utils.pretty_print(uri, response.text)
        state = ET.fromstring(response.text)
        return self.__parse_submitted_response(uri, state, resubmission_count)

    def __parse_submitted_response(
        self, uri: str, state: ET.Element, resubmission_count: int
    ) -> str:
        """
        Raises:
                RestfulFailure: If the status code of the response is not what was expected.
        """
        elements = state.findall("exits/exit")
        if 0 == len(elements):
            element = _get_valid_element(uri, state, "exited")
            if not 0 > resubmission_count:
                name_text = _get_valid_text(uri, element, "name")
                if "executing" == name_text:
                    if resubmission_count == RESUBMISSION_LIMIT:
                        raise RestfulFailure(
                            "re-submission limit has been reached, so this attempt will halt",
                            400,
                        )
                    uri_text = _get_valid_text(uri, element, "uri")
                    return self.__automatic_resubmission(
                        uri_text, resubmission_count + 1
                    )
                raise RestfulFailure(
                    "State that follows submission does not allow automatic re-submission, so this"
                    + " attempt will halt",
                    409,
                )
            raise RestfulFailure(
                "Another process has started processing this request, so this attempt will halt",
                409,
            )
        for exit_element in elements:
            name_text = _get_valid_text(uri, exit_element, "name")
            if "executing" == name_text:
                return _get_valid_text(uri, exit_element, "uri")
        raise RestfulFailure(
            f'Incomplete response returned from "{uri}", no "exit" element named "executing"',
            1,
        )

    def __processing_beginning(self, uri: str, message: str) -> Tuple[str, str]:
        """
        Informs the PSquared instance that processing is beginning for this
        item/version pairing.
        """
        state = self.__execute_transition(uri, message)
        elements = state.findall("exits/exit")
        for exit_element in elements:
            name_text = _get_valid_text(uri, exit_element, "name")
            if "processed" == name_text:
                processed_uri = _get_valid_text(uri, exit_element, "uri")
                break

        for exit_element in elements:
            name_text = _get_valid_text(uri, exit_element, "name")
            if "failed" == name_text:
                failed_uri = _get_valid_text(uri, exit_element, "uri")
                break

        return processed_uri, failed_uri
