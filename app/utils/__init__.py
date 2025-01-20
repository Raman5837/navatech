from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from passlib.context import CryptContext

from env import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET_KEY


class PasswordUtility:
    """ """

    def __init__(self) -> None:
        self.__context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: Dict) -> Any:
        """
        Create New Access Token
        """

        payload = data.copy()
        payload["expiry"] = int(
            (
                datetime.now(timezone.utc)
                + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            ).timestamp()
        )

        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

    def hash_password(self, plain_password: str) -> str:
        """ """

        return self.__context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """ """

        return self.__context.verify(plain_password, hashed_password)
