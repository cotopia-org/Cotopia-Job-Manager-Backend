import datetime
from os import getenv

import pytz
from dotenv import load_dotenv
from jose import jwt


def decode_token(token: str):
    load_dotenv()
    decoded = jwt.decode(token, getenv("SALT"), algorithms=["HS256"])
    if "is_genuine" in decoded:
        if decoded["is_genuine"] == getenv("PEPPER"):
            expires_at = datetime.datetime.strptime(
                decoded["expires_at"], "%Y-%m-%dT%H:%M:%S%z"
            )
            now = datetime.datetime.now(tz=pytz.utc)
            delta = expires_at - now
            if delta.total_seconds() > 0:
                del decoded["is_genuine"]
                return decoded
            else:
                return False
        else:
            return False
    else:
        return False
