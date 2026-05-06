from datetime import datetime, timedelta
import json
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model.database import Database
from model.mail import Mail
from model.otp import Otp, validate_otp
from model.token import Token, get_email_from_token
from model.user_data import fetch_user_data, fetch_admin_data, store_user_data

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
)

ValidateKeys = Literal["status", "token", "role"]
RequestKeys = Literal["status", "timeout"]
UploadKeys = Literal["status"]
DownloadKeys = Literal["status", "data"]


@app.post("/validate")
def validate(email: str, code: str) -> dict[ValidateKeys, str]:
    status = validate_otp(email, code)
    if status == "ok":
        token = "123456"
        # token = Token.generate()
        # encrypt token using otp in both ends
        Token.store(token, email)
        if email in admins:
            return {"status": status, "token": token, "role": "admin"}
        else:
            return {"status": status, "token": token, "role": "user"}
    return {"status": status}


@app.post("/request")
def request(email: str, length: int = 6) -> dict[RequestKeys, str]:
    # otp = Mail.send_otp(email, length)
    otp = Otp.generate(length)
    print(f"OTP is {otp}.")
    if otp == "":
        return {"status": "failed"}
    timeout = Otp.store(otp, email)
    return {"status": "ok", "timeout": str(timeout)}


class UserDataBody(BaseModel):
    token: str
    mood: float
    stress: float
    comment: str


@app.post("/upload")
def upload(payload: UserDataBody) -> dict[UploadKeys, str]:
    try:
        token = payload.token
        mood = payload.mood
        stress = payload.stress
        comment = payload.comment
        email = get_email_from_token(token)
        if email == "":
            return {"status": "unidentified token"}
        store_user_data(email, mood, stress, comment)
        return {"status": "ok"}
    except Exception:
        return {"status": "failed"}


@app.post("/download")
def download(token: str) -> dict[DownloadKeys, str]:
    email = get_email_from_token(token)
    if email == "":
        return {"status": "unidentified token"}
    now = datetime.now()
    time_stop = datetime(now.year, now.month, now.day)
    time_start = time_stop - timedelta(days=6)
    try:
        data = fetch_user_data(email, time_start, time_stop)
        return {"status": "ok", "data": json.dumps(data)}
    except:
        return {"status": "failed"}


admins = ["admin@uni.edu"]


@app.post("/admin")
def admin(token: str) -> dict[DownloadKeys, str]:
    email = get_email_from_token(token)
    if email == "":
        return {"status": "unidentified token"}
    elif email not in admins:
        return {"status": "not authorized"}

    now = datetime.now()
    time_stop = datetime(now.year, now.month, now.day)
    time_start = time_stop - timedelta(days=6)
    # try:
    data = fetch_admin_data(time_start, time_stop)
    return {"status": "ok", "data": json.dumps(data)}
    # except:
    #     return {"status": "failed"}


if __name__ == "__main__":
    # Database.drop_tables()
    # Database.create_tables()
    Database.add_dummies()
