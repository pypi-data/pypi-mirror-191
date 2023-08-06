from enum import Enum


class NotificationNotificationConfigHmacAlgorithm(str, Enum):
    hmac_sha512 = "hmac-sha512"
    hmac_sha384 = "hmac-sha384"
    hmac_sha256 = "hmac-sha256"
    hmac_sha1 = "hmac-sha1"

    def __str__(self) -> str:
        return str(self.value)
