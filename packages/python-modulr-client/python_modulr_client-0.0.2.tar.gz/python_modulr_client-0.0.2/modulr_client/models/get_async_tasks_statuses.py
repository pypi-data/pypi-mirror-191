from enum import Enum


class GetAsyncTasksStatuses(str, Enum):
    RECEIVED = "RECEIVED"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
    RUNNING = "RUNNING"

    def __str__(self) -> str:
        return str(self.value)
