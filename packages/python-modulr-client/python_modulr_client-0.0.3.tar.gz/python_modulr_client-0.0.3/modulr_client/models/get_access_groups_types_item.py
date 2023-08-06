from enum import Enum


class GetAccessGroupsTypesItem(str, Enum):
    DELEGATE = "DELEGATE"
    SERVICE_CUSTOMER = "SERVICE_CUSTOMER"
    USER_DEFINED = "USER_DEFINED"
    SERVICE_PARTNER = "SERVICE_PARTNER"

    def __str__(self) -> str:
        return str(self.value)
