import codecs
import hashlib
import hmac
import sys
import urllib.parse
from datetime import datetime
from wsgiref.handlers import format_date_time

if sys.version_info < (3, 8):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict

AuthorizationSignatureHeaders = TypedDict(
    "AuthorizationSignatureHeaders", {"Authorization": str, "Date": str, "x-mod-nonce": str}
)


def calculate(
    api_key: str, api_secret: str, nonce: str, timestamp: datetime
) -> AuthorizationSignatureHeaders:
    formatted_time = format_date_time(timestamp.timestamp())

    # Combines date and nonce into a single string that will be signed
    signature_string = "date" + ": " + formatted_time + "\n" + "x-mod-nonce" + ": " + nonce

    # Encodes secret and message into a format that can be signed
    secret = bytes(api_secret, encoding="utf-8")
    message = bytes(signature_string, encoding="utf-8")

    # Signing process
    digester = hmac.new(secret, message, hashlib.sha1)

    # Converts to hex
    signature = digester.hexdigest()

    # Decodes the signed string in hex into base64
    b64_signature = codecs.encode(codecs.decode(signature, "hex"), "base64").decode().strip()

    # Encodes the string so it is safe for URL
    url_safe_signature = urllib.parse.quote(b64_signature, safe="")

    # Adds the key and signed response
    authorisation = (
        f'Signature keyId="{api_key}",'
        'algorithm="hmac-sha1",'
        'headers="date x-mod-nonce",'
        f'signature="{url_safe_signature}"'
    )

    return {"Authorization": authorisation, "Date": formatted_time, "x-mod-nonce": nonce}
