from datetime import datetime, timedelta
from typing import Literal, Union

from Crypto.Random import random

from model.database import Database

StatusType = Literal["ok", "expired", "missing", "mismatch"]


class Otp:
    code: str
    email: str
    creation_time: datetime

    lifespan: timedelta = timedelta(minutes=5)

    def __init__(self, code: str, email: str) -> None:
        self.code = code
        self.email = email
        self.creation_time = datetime.now()

    def is_expired(self) -> bool:
        return datetime.now() - self.creation_time > self.lifespan

    @staticmethod
    def generate(length: int = 6) -> str:
        def pow10(n: int) -> int:
            r = 1
            for _ in range(n):
                r *= 10
            return r

        lower = pow10(length - 1)
        upper = lower * 10
        otp = random.randrange(lower, upper)
        return str(otp)

    def __str__(self) -> str:
        return str(self.code)

    @staticmethod
    def store(otp: str, email: str) -> int:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            # delete previously existing otp
            cursor.execute("delete from otp_data where email = ?", (email,))
            conn.commit()
            cursor.execute(
                "insert into otp_data values (?, ?, ?)",
                (otp, email, datetime.now().isoformat()),
            )
            conn.commit()
            return Otp.lifespan.seconds

    @staticmethod
    def fetch(email: str) -> Union["Otp", None]:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "select * from otp_data where email = ?",
                (email,),
            )
            result = cursor.fetchone()
            if result == None:
                return None
            if isinstance(result, tuple):
                otp_data = Otp(result[0], result[1])
                otp_data.creation_time = datetime.fromisoformat(result[2])
                return otp_data
            return None


def validate_otp(email: str, code: str) -> StatusType:
    otp = Otp.fetch(email)
    if otp == None:
        return "missing"
    if otp.code != code:
        return "mismatch"
    if otp.is_expired():
        return "expired"
    return "ok"
