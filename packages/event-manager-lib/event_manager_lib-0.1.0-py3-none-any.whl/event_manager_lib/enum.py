from enum import Enum


class Event(Enum):
    INTERNAL_ERROR = 1
    DATA_INGESTION_ERROR = 2
    RESOLVED = 3
