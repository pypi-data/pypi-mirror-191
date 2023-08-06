"""Provides mock responses for exercising the Engine"""

from typing import ByteString, Optional

import requests


def get(uri: str) -> requests.Response:
    """
    Return a mock response to a GET request, based on the supplied uri.
    """
    result = requests.Response()
    match uri:
        case _:
            text = """<realized-state>
    <exits>
        <exit>
            <name>executing</name>
            <uri>https://example.com/psquared/local/command/exit/1/executing</uri>
        </exit>
    </exits>
</realized-state>"""
    result.raw = MockResponse(text)
    result.status_code = 200
    return result


def post(uri: str) -> requests.Response:
    """
    Return a mock response to a POST request, based on the supplied uri.
    """
    result = requests.Response()
    if uri.endswith("executing"):
        text = """<realized-state>
    <exits>
        <exit>
            <name>processed</name>
            <uri>https://example.com/psquared/local/command/exit/2/processed</uri>
        </exit>
        <exit>
            <name>failed</name>
            <uri>https://example.com/psquared/local/command/exit/2/failed</uri>
        </exit>
    </exits>
</realized-state>"""
    elif uri.endswith("processed"):
        text = """<realized-state>
    <exits>
        <exit>
            <name>reset</name>
            <uri>https://example.com/psquared/local/command/exit/2/reset</uri>
        </exit>
    </exits>
</realized-state>"""

    else:
        raise ValueError("unknown URI")
    result.raw = MockResponse(text)
    result.status_code = 201
    return result


class MockResponse:  # pylint: disable=too-few-public-methods
    """
    This is used to mock up an HTTP response when testing this package.
    """

    def __init__(self, message: str):
        """
        Creates an instance of this class.

        Args:
            message: The string to return as the contents of this object.
        """
        self.__content = message.encode()
        self.__index = 0

    def read(self, amt: int) -> Optional[ByteString]:
        """
        Read the request amount of data
        """
        length = len(self.__content)
        if self.__index >= length:
            return None
        begin = self.__index
        end = self.__index + amt
        end = min(end, length)
        self.__index = end - begin
        return self.__content[begin:end]
