from enum import Enum


class AccountAssociateResponseVerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    EXVERIFIED = "EXVERIFIED"
    REVIEWED = "REVIEWED"
    REFERRED = "REFERRED"
    MIGRATED = "MIGRATED"
    DECLINED = "DECLINED"

    def __str__(self) -> str:
        return str(self.value)
