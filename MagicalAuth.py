# uvicorn app:server --port 14374 --workers 4
# streamlit run UI.py
from DB import User, FailedLogins, get_session
import os
import pyotp
import requests
import base64
from hashlib import md5
from Crypto.Cipher import AES
from datetime import datetime, timedelta
from fastapi import HTTPException
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
- ENCRYPTION_SECRET: Encryption key to encrypt and decrypt data
- MAGIC_LINK_URL: URL to send in the email for the user to click on
- REGISTRATION_WEBHOOK: URL to send a POST request to when a user registers
- ALLOWED_DOMAINS: Comma separated list of allowed domains for registration
"""


def send_email(
    email: str,
    subject: str,
    body: str,
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
    return None


def encrypt(passphrase, data):
    passphrase = passphrase.encode("utf-8")
    salt = os.urandom(8)
    passphrase += salt
    key = md5(passphrase).digest()
    final_key = key
    while len(final_key) < 32 + 16:
        key = md5(key + passphrase).digest()
        final_key += key
    key_iv = final_key[: 32 + 16]
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    padded_data = data.encode("utf-8") + (16 - len(data) % 16) * bytes(
        [16 - len(data) % 16]
    )
    encrypted_data = aes.encrypt(padded_data)
    encrypted = b"Salted__" + salt + encrypted_data
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt(passphrase, data):
    try:
        passphrase = passphrase.encode("utf-8")
        encrypted = base64.b64decode(data)
        assert encrypted[0:8] == b"Salted__"
        salt = encrypted[8:16]
        assert len(salt) == 8, len(salt)
        passphrase += salt
        key = md5(passphrase).digest()
        final_key = key
        while len(final_key) < 32 + 16:
            key = md5(key + passphrase).digest()
            final_key += key
        key_iv = final_key[: 32 + 16]
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        data = aes.decrypt(encrypted[16:])
        decrypted = data[: -(data[-1] if type(data[-1]) == int else ord(data[-1]))]
        return decrypted.decode("utf-8")
    except:
        return data


class MagicalAuth:
    def __init__(self, email: str, token: str = None):
        encryption_key = os.environ.get("ENCRYPTION_SECRET", "")
        self.link = os.environ.get("MAGIC_LINK_URL", "https://localhost:8507/")
        self.encryption_key = f'{encryption_key}{datetime.now().strftime("%Y%m%d")}'
        self.email = email.lower()
        self.token = (
            token.replace("%2B", "+")
            .replace("%2F", "/")
            .replace("%3D", "=")
            .replace("%20", " ")
            .replace("%3A", ":")
            .replace("%3F", "?")
            .replace("%26", "&")
            .replace("%23", "#")
            .replace("%3B", ";")
            .replace("%40", "@")
            .replace("%21", "!")
            .replace("%24", "$")
            .replace("%27", "'")
            .replace("%28", "(")
            .replace("%29", ")")
            .replace("%2A", "*")
            .replace("%2C", ",")
            .replace("%3B", ";")
            .replace("%5B", "[")
            .replace("%5D", "]")
            .replace("%7B", "{")
            .replace("%7D", "}")
            .replace("%7C", "|")
            .replace("%5C", "\\")
            .replace("%5E", "^")
            .replace("%60", "`")
            .replace("%7E", "~")
            if token
            else None
        )

    def add_failed_login(self, ip_address):
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        if user is not None:
            failed_login = FailedLogins(user_id=user.id, ip_address=ip_address)
            session.add(failed_login)
            session.commit()
        session.close()

    def count_failed_logins(self):
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        if user is None:
            session.close()
            return 0
        failed_logins = (
            session.query(FailedLogins)
            .filter(FailedLogins.user_id == user.id)
            .filter(FailedLogins.created_at >= datetime.now() - timedelta(hours=24))
            .count()
        )
        session.close()
        return failed_logins

    def send_magic_link(self, otp, ip_address):
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        session.close()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        self.token = encrypt(
            passphrase=f"{self.encryption_key}{str(user.id)}", data=str(user.id)
        )
        if not pyotp.TOTP(user.mfa_token).verify(otp):
            self.add_failed_login(ip_address=ip_address)
            raise HTTPException(
                status_code=401, detail="Invalid MFA token. Please try again."
            )
        token = (
            self.token.replace("+", "%2B")
            .replace("/", "%2F")
            .replace("=", "%3D")
            .replace(" ", "%20")
            .replace(":", "%3A")
            .replace("?", "%3F")
            .replace("&", "%26")
            .replace("#", "%23")
            .replace(";", "%3B")
            .replace("@", "%40")
            .replace("!", "%21")
            .replace("$", "%24")
            .replace("'", "%27")
            .replace("(", "%28")
            .replace(")", "%29")
            .replace("*", "%2A")
            .replace(",", "%2C")
            .replace(";", "%3B")
            .replace("[", "%5B")
            .replace("]", "%5D")
            .replace("{", "%7B")
            .replace("}", "%7D")
            .replace("|", "%7C")
            .replace("\\", "%5C")
            .replace("^", "%5E")
            .replace("`", "%60")
            .replace("~", "%7E")
        )
        magic_link = f"{self.link}?email={self.email}&token={token}"
        if os.environ.get("SENDGRID_API_KEY"):
            send_email(
                email=self.email,
                subject="Magic Link",
                body=f"<a href='{magic_link}'>Click here to log in</a>",
            )
        else:
            return magic_link
        # Upon clicking the link, the front end will call the login method and save the email and encrypted_id in the session
        return f"A login link has been sent to {self.email}, please check your email and click the link to log in. The link will expire in 24 hours."

    def login(self, ip_address):
        """ "
        Login method to verify the token and return the user object

        :param ip_address: IP address of the user
        :return: User object
        """
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        session.close()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        failures = self.count_failed_logins()
        if failures >= 50:
            raise HTTPException(
                status_code=429,
                detail="Too many failed login attempts today. Please try again tomorrow.",
            )
        user_id = decrypt(
            passphrase=f"{self.encryption_key}{str(user.id)}", data=self.token
        )
        if str(user.id) == user_id:
            return user
        self.add_failed_login(ip_address=ip_address)
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
        allowed_domains = os.environ.get("ALLOWED_DOMAINS", "*")
        if allowed_domains != "*":
            if "," in allowed_domains:
                allowed_domains = allowed_domains.split(",")
            else:
                allowed_domains = [allowed_domains]
            domain = self.email.split("@")[1]
            if domain not in allowed_domains:
                raise HTTPException(
                    status_code=403,
                    detail="Registration is not allowed for this domain.",
                )
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
            requests.post(
                registration_webhook,
                json={"email": self.email},
                headers={"Authorization": os.environ.get("ENCRYPTION_SECRET", "")},
            )
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

    def delete_user(self):
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        if user is None:
            session.close()
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = False
        session.commit()
        session.close()
        return "User deleted successfully"
