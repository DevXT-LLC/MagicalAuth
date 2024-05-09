from DB import User, get_session
import os
import pyotp
import requests
from datetime import datetime
from fastapi import HTTPException
from gtauthclient import GTAuthClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    Mail,
)

"""
Required environment variables:

- SENDGRID_API_KEY: SendGrid API key
- SENDGRID_FROM_EMAIL: Default email address to send emails from
- ENCRYPTION_SECRET: Encryption key for the GTAuthClient
- MAGIC_LINK_URL: URL to send in the email for the user to click on
- REGISTRATION_WEBHOOK: URL to send a POST request to when a user registers
"""


def send_email(
    email,
    subject,
    body,
    attachment_content=None,
    attachment_file_type=None,
    attachment_file_name=None,
):
    message = Mail(
        from_email=os.environ.get("SENDGRID_FROM_EMAIL"),
        to_emails=email,
        subject=subject,
        html_content=body,
    )
    if (
        attachment_content != None
        and attachment_file_type != None
        and attachment_file_name != None
    ):
        attachment = Attachment(
            FileContent(attachment_content),
            FileName(attachment_file_name),
            FileType(attachment_file_type),
            Disposition("attachment"),
        )
        message.attachment = attachment
    response = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY")).send(message)
    if response.status_code != 202:
        raise HTTPException(status_code=400, detail="Email could not be sent.")


class MagicalAuth:
    def __init__(self, email: str, token: str = None):
        encryption_key = os.environ.get("ENCRYPTION_SECRET", "")
        self.link = os.environ.get("MAGIC_LINK_URL", "https://localhost:8501/")
        self.encryption_key = f'{encryption_key}{datetime.now().strftime("%Y%m%d")}'
        self.email = email.lower()
        self.token = token

    def send_magic_link(self, otp):
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        session.close()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        self.token = GTAuthClient(key=f"{self.encryption_key}{user.id}").encrypt(
            data=user.id
        )
        if not pyotp.TOTP(user.mfa_token).verify(otp):
            raise HTTPException(
                status_code=401, detail="Invalid MFA token. Please try again."
            )
        send_email(
            email=self.email,
            message=f"<a href='{self.link}?email={self.email}&token={self.token}'>Click here to log in</a>",
        )
        # Upon clicking the link, the front end will call the login method and save the email and encrypted_id in the session
        return f"A login link has been sent to {self.email}, please check your email and click the link to log in. The link will expire in 24 hours."

    def login(self):
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        session.close()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = GTAuthClient(key=f"{self.encryption_key}{user.id}").decrypt(
            data=self.token
        )
        if str(user.id) == user_id:
            return user
        raise HTTPException(
            status_code=418,
            detail="Invalid login token. Please log out and try again.",
        )

    def register(
        self,
        first_name: str,
        last_name: str,
        company_name: str,
        job_title: str,
    ):
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        if user is not None:
            session.close()
            raise HTTPException(
                status_code=409, detail="User already exists with this email."
            )
        mfa_token = pyotp.random_base32()
        user = User(
            mfa_token=mfa_token,
            email=self.email,
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            job_title=job_title,
        )
        session.add(user)
        session.commit()
        session.close()
        # Send registration webhook out to third party application such as AGiXT to create a user there.
        registration_webhook = os.environ.get("REGISTRATION_WEBHOOK", "")
        if registration_webhook:
            requests.post(registration_webhook, json={"email": self.email})
        # Return mfa_token for QR code generation
        return mfa_token

    def update_user(self, **kwargs):
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        if user is None:
            session.close()
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in kwargs.items():
            if key in ["first_name", "last_name", "company_name", "job_title"]:
                setattr(user, key, value)
        session.commit()
        session.close()
        return "User updated successfully"
