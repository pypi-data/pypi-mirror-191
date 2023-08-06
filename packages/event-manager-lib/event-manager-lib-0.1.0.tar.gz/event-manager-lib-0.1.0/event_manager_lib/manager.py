import logging
from dataclasses import dataclass

from event_manager_lib.enum import Event

logger = logging.getLogger("event-manager-library")


@dataclass
class EventManager:
    topic: str
    queue_url: str

    def send_message(self, message: str, event_type: Event) -> None:
        """dispatch messsage to the message queue

        Raises:
            TypeError - invalid type for input parameter
        """
        if not isinstance(message, str):
            raise TypeError(
                f"{self.__class__.__name__}.send_message(), invalid input type for 'message', expected {type(str)}, got {type(message)}")

        if not isinstance(event_type, Event):
            raise TypeError(
                f"{self.__class__.__name__}.send_message(), invalid input type for 'event_type', expected {type(Event)}, got {type(message)}")

        logger.debug(
            f"dispatch of new message to topic: {self.topic}, message queue URL: {self.queue_url}, event type: {event_type.name}, message: {message}")
