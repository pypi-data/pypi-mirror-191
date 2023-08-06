"""Provide utilities to help using the psquared_consume package"""

from typing import Dict

from argparse import Namespace
import os
import sys


def eprint(*args, **kwargs) -> None:
    """
    Print message to stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def pretty_print(uri: str, document: str, response=True):
    """
    Simple pretty print for *IX systems to the error stream.

    Args:
        uri: The uri to which the request was made.
        document: The XML document to print.
        response: True if the document is a response to a request,
                otherwise it is treated as the payload to a request.
    """
    if None is not uri:
        if response:
            eprint("URI : Response : " + uri)
        else:
            eprint("URI : Request :  " + uri)
    #    print(document)
    os.system(f"echo '{document}' | xmllint -format - 1>&2")
    eprint("--------")


def read_envar_values(mapping: Dict[str, str]):
    """
    Create a argparse.Namespace instance populated by the values of the
    envrionmental variables specified by the keys of the mapping.
    """
    result = {}
    for key in mapping.keys():
        value = os.getenv(key)
        if None is not value:
            option = mapping[key]
            result[option] = value
    return Namespace(**result)
