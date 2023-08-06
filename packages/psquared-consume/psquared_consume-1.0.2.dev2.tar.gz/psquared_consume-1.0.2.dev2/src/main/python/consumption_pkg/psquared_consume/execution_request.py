"""
Defined the ExecutionRequest class.
"""

from typing import List, Optional

import errno
import io
import os
import xml.etree.ElementTree as ET


class RestfulFailure(Exception):
    """
    Thrown when document can not be parses to create a
        ExecutionRequest instance.
    """

    def __init__(self, message):
        Exception.__init__(self, message)


def _build_string(element: Optional[ET.Element]) -> Optional[str]:
    """
    Builds a string from a ElementTree Element.

    Args:
        element: the ElementTree Elements from which to build the
                result.
    """
    if None is element or "" == element.text:
        return None
    return element.text


def _build_strings(
    elements: Optional[List[ET.Element]],
) -> Optional[List[str]]:
    """
    Builds a List of string from a set of ElementTree Elements.

    Args:
        args: the List of ElementTree Elements from which to build
                the result.
    Returns:
        the List of string from a set of ElementTree Elements.

    Raises:
        ValueError: If any of the string are None.
    """
    if None is elements or 0 == len(elements):
        return None
    arguments: List[str] = []
    for element in elements:
        text = _build_string(element)
        if None is text:
            raise ValueError("The string are not optional in the List")
        arguments.append(text)
    return arguments


def _mkdirs(path: str) -> None:
    """
    Makes sure the supplied directory exists, creating it if necessary.

    Args:
        path: The path to the directory.
    """
    try:
        os.makedirs(path)
    except OSError as os_error:
        if os_error.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise os_error


def _open_file(path: str) -> Optional[io.TextIOWrapper]:
    """
    Opens a file at the supplied path, creating any directory that does
    not exist. Relative paths are create with respect to the HOME
    directory of the user.

    Args:
        path: The path to the file.
    """
    if path.startswith("/"):
        filepath = path
    else:
        if "PSQUARED_HOME" in os.environ:
            filepath = os.environ["PSQUARED_HOME"] + os.sep + path
        else:
            filepath = os.path.expanduser("~/" + path)
    directory = os.path.dirname(filepath)
    if None is not directory and "" != directory:
        _mkdirs(directory)
    return open(filepath, "w")  # pylint: disable=unspecified-encoding


class ExecutionRequest:  # pylint: disable=too-few-public-methods
    """
    This class encapsulates a requests from PSquared to execute a command.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        submission_uri: str,
        cmd: str,
        arguments: Optional[List[str]] = None,
        success_cmd: Optional[str] = None,
        failure_cmd: Optional[str] = None,
        cmd_out: Optional[io.TextIOWrapper] = None,
        cmd_err: Optional[io.TextIOWrapper] = None,
    ):
        """
        Create an instance of this class.

        Args:
            submission_url: The URI of the submission request for
                this execution.
            cmd: The command to be executed in order to satisfy this
                request.
            arguments: The sequence of arguments to be passed to the
                commands.
            success_cmd: The command, if any, to execute if this
                request succeeds.
            failure_cmd: The command, if any, to execute if this
                request fails.
            cmd_out: The path, if any, to use at the standard output
                when executing the request.
            cmd_err: The path, if any, to use at the standard error
                when executing the request.
        """
        self.submission_uri = submission_uri
        self.cmd = cmd
        self.success_cmd = success_cmd
        self.failure_cmd = failure_cmd
        self.arguments = arguments
        self.cmd_out = cmd_out
        self.cmd_err = cmd_err


def parse_xml(document: ET.Element) -> ExecutionRequest:
    """
    Creates an ExecutionRequest instance by parsing the supplied XML.

    Raises:
        ValueError: If the element does not contain a valid
                ExecutionRequest.
    """
    element = document.find("submission_uri")
    if None is element:
        raise ValueError('There is no "submission_uri" in the document')
    text = element.text
    if None is text or "" == text:
        raise ValueError('There is no "submission_uri" in the document')
    submission_uri: str = text

    element = document.find("command")
    if None is element:
        raise ValueError('There is no "command" in the document')
    text = element.text
    if None is text or "" == text:
        raise ValueError('There is no "command" in the document')
    cmd: str = text
    args = document.findall("argument")
    arguments = _build_strings(args)
    element = document.find("success_cmd")
    success_cmd = _build_string(element)
    element = document.find("failure_cmd")
    failure_cmd = _build_string(element)
    filepath = document.get("stdout")
    if None is filepath:
        cmd_out = None
    else:
        cmd_out = _open_file(filepath)
    filepath = document.get("stderr")
    if None is filepath:
        cmd_err = None
    else:
        cmd_err = _open_file(filepath)
    return ExecutionRequest(
        submission_uri,
        cmd,
        arguments,
        success_cmd,
        failure_cmd,
        cmd_out,
        cmd_err,
    )
