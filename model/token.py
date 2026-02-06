import base64
from datetime import datetime, timedelta
from typing import Union

from Crypto.Random import get_random_bytes

from model.database import Database


class Token:
    token: str
    email: str
    creation_time: datetime

    lifespan: timedelta = timedelta(minutes=20)

    def __init__(self, token: str, email: str) -> None:
        self.token = token
        self.email = email
        self.creation_time = datetime.now()

    def is_expired(self) -> bool:
        return datetime.now() - self.creation_time > self.lifespan

    @staticmethod
    def generate(bytesize: int = 32) -> str:
        token = base64.urlsafe_b64encode(get_random_bytes(bytesize))
        return token.decode()

    @staticmethod
    def store(token: str, email: str) -> int:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            # delete previously existing token
            cursor.execute("delete from token_data where email = ?", (email,))
            cursor.execute(
                "insert into token_data values (?, ?, ?)",
                (token, email, datetime.now().isoformat()),
            )
            conn.commit()
            return Token.lifespan.seconds

    @staticmethod
    def fetch(token: str) -> Union["Token", None]:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("select * from token_data where token = ?", (token,))
            result = cursor.fetchone()
            if result == None:
                return None
            if isinstance(result, tuple):
                token_data = Token(result[0], result[1])
                token_data.creation_time = datetime.fromisoformat(result[2])
                return token_data
            return None


def get_email_from_token(token: str) -> str:
    token_data = Token.fetch(token)
    if token_data == None:
        return ""
    if not token_data.is_expired():
        return token_data.email
    return ""
