"""A command line interface to run an instance of the PSquared state machine."""

import argparse
import logging
import socket
import sys

import requests

from .execution_request import ExecutionRequest
from .psquared_engine import Engine, RestfulFailure
from . import utils

_ENVARS_MAPPING = {
    "PP_ENGINE_LOG_FILE": "LOG_FILE",
    "PP_ENGINE_LOG_LEVEL": "LOG_LEVEL",
}

_LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def _create_argument_parser() -> argparse.ArgumentParser:
    """
    Creates and populated the argparse.ArgumentParser for this executable.
    """
    parser = argparse.ArgumentParser(
        description="Executes an instance of a rabbit_consume.pusher class"
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="DEBUG",
        help="print out detail information to stdout, automatically set log level to DEBUG.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--log_file",
        dest="LOG_FILE",
        help="The file, as opposed to stdout, into which to write log messages",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        default="INFO",
        dest="LOG_LEVEL",
        help="The logging level for this execution",
        choices=_LOG_LEVELS.keys(),
    )
    parser.add_argument(
        "-s",
        "--success_cmd",
        dest="SUCCESS_CMD",
        help="The command to run after a successful processing",
        default=None,
    )
    parser.add_argument(
        "-f",
        "--failure_cmd",
        dest="FAILURE_CMD",
        help="The command to run after a failed processing",
        default=None,
    )
    parser.add_argument(
        "-o",
        dest="OUTPUT",
        type=argparse.FileType("a"),
        help="The file, as opposed to stdout, into which to write the output of the command",
        default=None,
    )
    parser.add_argument(
        "-e",
        dest="ERROR",
        type=argparse.FileType("a"),
        help="The file, as opposed to stderr, into which to write errors from the command",
        default=None,
    )
    parser.add_argument(
        "-r",
        "--resubmission",
        dest="RESUBMISSION",
        help="allows automatic re-submission to take place.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "submission_url",
        help="The submission URL used to create the processing request to be handled",
    )
    parser.add_argument("cmd", help="The command to be executed")
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="An argument to the command to be executed",
    )
    return parser


def main():
    """
    A command line interface to run an instance of the PSquared state machine.
    """
    parser = _create_argument_parser()
    envar_values = utils.read_envar_values(_ENVARS_MAPPING)
    options = parser.parse_args(namespace=envar_values)

    if None is options.LOG_FILE:
        logging.basicConfig(stream=sys.stdout, level=_LOG_LEVELS[options.LOG_LEVEL])
    else:
        logging.basicConfig(
            filename=options.LOG_FILE, level=_LOG_LEVELS[options.LOG_LEVEL]
        )

    logging.debug("Begin options:")
    for option in options.__dict__:
        if options.__dict__[option] is not None:
            logging.debug("    %s = %s", option, options.__dict__[option])
    logging.debug("End options:")

    logging.info("BEGIN CONSUMPTION")
    try:
        request = ExecutionRequest(
            options.submission_url,
            options.cmd,
            options.args,
            options.SUCCESS_CMD,
            options.FAILURE_CMD,
            options.OUTPUT,
            options.ERROR,
        )
        engine = Engine(options.DEBUG)
        engine.execute(
            "Executing on " + socket.gethostname() + " using pp_engine.py",
            request,
            options.RESUBMISSION,
        )
        logging.info("END CONSUMPTION")
    except requests.exceptions.ConnectionError:
        logging.error(
            "Could not connection to PSquared server with url %s",
            options.submission_url,
        )
        logging.info("ABORT CONSUMPTION")
    except RestfulFailure as psquared_failure:
        logging.error("Failed to complete state machine")
        logging.exception(psquared_failure)
        utils.eprint("Failed in PSquared:\n", psquared_failure)
        logging.info("FAIL CONSUMPTION")
    except Exception as abort_exception:  #  pylint: disable=broad-except
        logging.error("Aborted while in state machine")
        logging.exception(abort_exception)
        utils.eprint("Aborted in PSquared:\n", abort_exception)
        logging.info("ABORT CONSUMPTION")
