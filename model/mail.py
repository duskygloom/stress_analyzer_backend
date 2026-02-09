from email.message import EmailMessage
import os
import smtplib

import dotenv

from model.otp import Otp

if os.path.exists(".env"):
    dotenv.load_dotenv(".env")

USERNAME = str(os.getenv("EMAIL_ADDRESS"))
PASSWORD = str(os.getenv("EMAIL_PASSWORD"))


class Mail:
    @staticmethod
    def send_otp(recepient: str, length: int) -> str:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            try:
                server.login(USERNAME, PASSWORD)
                message = EmailMessage()
                message["From"] = USERNAME
                message["To"] = recepient
                message["Subject"] = "One Time Password"
                otp = Otp.generate(length)
                message.set_content(
                    f"Your OTP is {otp}.\n"
                    f"It will expire in {Otp.lifespan.seconds} seconds."
                )
                server.send_message(message)
                return otp
            except Exception:
                return ""
