"""
Defines the PrintConsumption class.
"""

import logging
import socket
import xml.etree.ElementTree as ET

from pika.spec import BasicProperties

from .execution_request import parse_xml
from .psquared_engine import Engine, RestfulFailure
from . import utils


class PSquaredConsumption:
    """
    This implementation of the rabbitmq-consume Consumption Protocol
        the consume PSquared messages and satifying the execution
        request contained within.
    """

    def __init__(
        self,
        _: BasicProperties,
        body: bytes,
        delivery_tag: int,
        redelivered: bool,
    ):
        """
        Creates a Consumption instance of the class that will consume
        the body.

        Args:
            _: The properties of the message.
            body: the XML body of the RabbitMQ message to be consumed
                by the created Consumption instance.
            delivery_tag: The tag identifying the RabbitMQ message.
            redelivered: True if the supplied body has been delivered
                before.
        """
        self.__document = ET.fromstring(body)
        self.__delivery_tag = delivery_tag
        self.__redelivered = redelivered

    def consume(self) -> None:  #  pylint: disable=too-many-locals
        """
        Consumes the XML body of a RabbitMQ message.
        """
        logging.info("BEGIN CONSUMPTION")

        try:
            action = self.__document.get("action")
            if "ignore" == action:
                logging.info(
                    'Ignoring execution request as specified by its "action" element'
                )
            else:
                request = parse_xml(self.__document)
                logging.debug("Beginning state machine completion")
                engine = Engine()
                engine.execute(self.__execution_message(), request, self.__redelivered)
                logging.info("END CONSUMPTION")
        except RestfulFailure as restful_failure:
            logging.error("Failed to complete state machine")
            logging.exception(restful_failure)
            utils.eprint("Failed in PSquared:\n", restful_failure)
            logging.info("FAIL CONSUMPTION")
        except Exception as abort_exception:  #  pylint: disable=broad-except
            logging.error("Aborted while in state machine")
            logging.exception(abort_exception)
            utils.eprint("Aborted in PSquared:\n", abort_exception)
            logging.info("ABORT CONSUMPTION")

    def delivery_tag(self) -> int:
        """
        Returns the tag identifying the RabbitMQ message.
        """
        return self.__delivery_tag

    def __execution_message(self) -> str:
        return "Executing on " + socket.gethostname()
