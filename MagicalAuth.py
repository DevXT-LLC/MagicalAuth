from DB import User, FailedLogins, UserOAuth, OAuthProvider, get_session
from Models import UserInfo, Register, Login
from fastapi import Header, HTTPException
from Globals import getenv
from OAuth2Providers import get_sso_provider
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
import pyotp
import requests
import logging
import jwt


logging.basicConfig(
    level=getenv("LOG_LEVEL"),
    format=getenv("LOG_FORMAT"),
)
"""
Required environment variables:

- SENDGRID_API_KEY: SendGrid API key
- SENDGRID_FROM_EMAIL: Default email address to send emails from
- ENCRYPTION_SECRET: Encryption key to encrypt and decrypt data
- MAGIC_LINK_URL: URL to send in the email for the user to click on
- REGISTRATION_WEBHOOK: URL to send a POST request to when a user registers
"""


def verify_api_key(authorization: str = Header(None)):
    ENCRYPTION_SECRET = getenv("ENCRYPTION_SECRET")
    if getenv("AUTH_PROVIDER") == "magicalauth":
        ENCRYPTION_SECRET = f'{ENCRYPTION_SECRET}{datetime.now().strftime("%Y%m%d")}'
    authorization = str(authorization).replace("Bearer ", "").replace("bearer ", "")
    if ENCRYPTION_SECRET:
        if authorization is None:
            raise HTTPException(
                status_code=401, detail="Authorization header is missing"
            )
        if authorization == ENCRYPTION_SECRET:
            return "ADMIN"
        try:
            if authorization == ENCRYPTION_SECRET:
                return "ADMIN"
            token = jwt.decode(
                jwt=authorization,
                key=ENCRYPTION_SECRET,
                algorithms=["HS256"],
                leeway=timedelta(hours=5),
            )
            db = get_session()
            user = db.query(User).filter(User.id == token["sub"]).first()
            db.close()
            return user
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid API Key")
    else:
        return authorization


def send_email(
    email: str,
    subject: str,
    body: str,
    attachment_content=None,
    attachment_file_type=None,
    attachment_file_name=None,
):
    message = Mail(
        from_email=getenv("SENDGRID_FROM_EMAIL"),
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

    try:
        response = SendGridAPIClient(getenv("SENDGRID_API_KEY")).send(message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Email could not be sent.")
    if response.status_code != 202:
        raise HTTPException(status_code=400, detail="Email could not be sent.")
    return None


class MagicalAuth:
    def __init__(self, token: str = None):
        encryption_key = getenv("ENCRYPTION_SECRET")
        self.link = getenv("MAGIC_LINK_URL")
        self.encryption_key = f'{encryption_key}{datetime.now().strftime("%Y%m%d")}'
        self.token = (
            str(token)
            .replace("%2B", "+")
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
            .replace("Bearer ", "")
            .replace("bearer ", "")
            if token
            else None
        )
        try:
            # Decode jwt
            decoded = jwt.decode(
                jwt=token,
                key=self.encryption_key,
                algorithms=["HS256"],
                leeway=timedelta(hours=5),
            )
            self.email = decoded["email"]
            self.token = token
        except:
            self.email = None
            self.token = None

    def user_exists(self, email: str = None):
        self.email = email.lower()
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        session.close()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return True

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

    def send_magic_link(
        self,
        ip_address,
        login: Login,
        referrer=None,
        send_link: bool = True,
    ):
        self.email = login.email.lower()
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        session.close()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not pyotp.TOTP(user.mfa_token).verify(login.token):
            self.add_failed_login(ip_address=ip_address)
            raise HTTPException(
                status_code=401, detail="Invalid MFA token. Please try again."
            )
        self.token = jwt.encode(
            {
                "sub": str(user.id),
                "email": self.email,
                "admin": user.admin,
                "exp": datetime.utcnow() + timedelta(hours=24),
            },
            self.encryption_key,
            algorithm="HS256",
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
        if referrer is not None:
            self.link = referrer
        magic_link = f"{self.link}?token={token}"
        if (
            getenv("SENDGRID_API_KEY") != ""
            and str(getenv("SENDGRID_API_KEY")).lower() != "none"
            and getenv("SENDGRID_FROM_EMAIL") != ""
            and str(getenv("SENDGRID_FROM_EMAIL")).lower() != "none"
            and send_link
        ):
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
        failures = self.count_failed_logins()
        if failures >= 50:
            raise HTTPException(
                status_code=429,
                detail="Too many failed login attempts today. Please try again tomorrow.",
            )
        try:
            user_info = jwt.decode(
                jwt=self.token,
                key=self.encryption_key,
                algorithms=["HS256"],
                leeway=timedelta(hours=5),
            )
        except:
            self.add_failed_login(ip_address=ip_address)
            raise HTTPException(
                status_code=401,
                detail="Invalid login token. Please log out and try again.",
            )
        user_id = user_info["sub"]
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if str(user.id) == str(user_id):
            return user
        self.add_failed_login(ip_address=ip_address)
        raise HTTPException(
            status_code=401,
            detail="Invalid login token. Please log out and try again.",
        )

    def register(
        self,
        new_user: Register,
    ):
        new_user.email = new_user.email.lower()
        self.email = new_user.email
        allowed_domains = getenv("ALLOWED_DOMAINS")
        if allowed_domains is None or allowed_domains == "":
            allowed_domains = "*"
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
            **new_user.model_dump(),
        )
        session.add(user)
        session.commit()
        session.close()
        # Send registration webhook out to third party application such as AGiXT to create a user there.
        registration_webhook = getenv("REGISTRATION_WEBHOOK")
        if registration_webhook:
            try:
                requests.post(
                    registration_webhook,
                    json={"email": self.email},
                    headers={"Authorization": getenv("ENCRYPTION_SECRET")},
                )
            except Exception as e:
                pass
        # Return mfa_token for QR code generation
        return mfa_token

    def update_user(self, **kwargs):
        user = verify_api_key(self.token)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        session = get_session()
        user = session.query(User).filter(User.id == user.id).first()
        allowed_keys = list(UserInfo.__annotations__.keys())
        for key, value in kwargs.items():
            if key in allowed_keys:
                setattr(user, key, value)
        session.commit()
        session.close()
        return "User updated successfully"

    def delete_user(self):
        user = verify_api_key(self.token)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        session = get_session()
        user = session.query(User).filter(User.id == user.id).first()
        user.is_active = False
        session.commit()
        session.close()
        return "User deleted successfully"

    def sso(
        self,
        provider,
        code,
        ip_address,
        referrer=None,
    ):
        if not referrer:
            referrer = getenv("MAGIC_LINK_URL")
        provider = str(provider).lower()
        sso_data = None
        sso_data = get_sso_provider(provider=provider, code=code, redirect_uri=referrer)
        if not sso_data:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to get user data from {provider.capitalize()}.",
            )
        if not sso_data.access_token:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to get access token from {provider.capitalize()}.",
            )
        user_data = sso_data.user_info
        access_token = sso_data.access_token
        refresh_token = sso_data.refresh_token
        self.email = str(user_data["email"]).lower()
        if not user_data:
            logging.warning(f"Error on {provider.capitalize()}: {user_data}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to get user data from {provider.capitalize()}.",
            )
        session = get_session()
        user = session.query(User).filter(User.email == self.email).first()
        if not user:
            register = Register(
                email=self.email,
                first_name=user_data["first_name"] if "first_name" in user_data else "",
                last_name=user_data["last_name"] if "last_name" in user_data else "",
            )
            mfa_token = self.register(new_user=register)
            # Create the UserOAuth record
            user = session.query(User).filter(User.email == self.email).first()
            provider = (
                session.query(OAuthProvider)
                .filter(OAuthProvider.name == provider)
                .first()
            )
            if not provider:
                provider = OAuthProvider(name=provider)
                session.add(provider)
            user_oauth = UserOAuth(
                user_id=user.id,
                provider_id=provider.id,
                access_token=access_token,
                refresh_token=refresh_token,
            )
            session.add(user_oauth)
        else:
            mfa_token = user.mfa_token
            user_oauth = (
                session.query(UserOAuth).filter(UserOAuth.user_id == user.id).first()
            )
            if user_oauth:
                user_oauth.access_token = access_token
                user_oauth.refresh_token = refresh_token
        session.commit()
        session.close()
        totp = pyotp.TOTP(mfa_token)
        login = Login(email=self.email, token=totp.now())
        return self.send_magic_link(
            ip_address=ip_address,
            login=login,
            referrer=referrer,
            send_link=False,
        )
