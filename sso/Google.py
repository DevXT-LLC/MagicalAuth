import base64
import json
import requests
import logging
from email.mime.text import MIMEText
from Globals import getenv

"""
Required environment variables:

- GOOGLE_CLIENT_ID: Google OAuth client ID
- GOOGLE_CLIENT_SECRET: Google OAuth client secret

Required APIs

Follow the links to confirm that you have the APIs enabled,
then add the `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` environment variables to your `.env` file.

- People API https://console.cloud.google.com/marketplace/product/google/people.googleapis.com
- Gmail API https://console.cloud.google.com/marketplace/product/google/gmail.googleapis.com

Required scopes for Google SSO

- https://www.googleapis.com/auth/userinfo.profile
- https://www.googleapis.com/auth/gmail.send
"""


def get_google_access_token(code, redirect_uri=None):
    if not redirect_uri:
        redirect_uri = getenv("MAGIC_LINK_URL")
    code = (
        str(code)
        .replace("%2F", "/")
        .replace("%3D", "=")
        .replace("%3F", "?")
        .replace("%3D", "=")
    )
    response = requests.post(
        f"https://accounts.google.com/o/oauth2/token",
        params={
            "code": code,
            "client_id": getenv("GOOGLE_CLIENT_ID"),
            "client_secret": getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    if response.status_code != 200:
        logging.error(f"Error getting Google access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    return access_token, refresh_token


class GoogleSSO:
    def __init__(
        self,
        access_token=None,
        refresh_token=None,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        if not self.access_token:
            raise Exception("Invalid code")
        self.client_id = getenv("GOOGLE_CLIENT_ID")
        self.client_secret = getenv("GOOGLE_CLIENT_SECRET")
        self.email_address = ""

    def get_new_token(self):
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            },
        )
        return response.json()["access_token"]

    def get_user_info(self):
        response = requests.get(
            "https://people.googleapis.com/v1/people/me",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.get(
                "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,organizations",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        data = response.json()
        logging.info(f"Google user info: {data}")
        return {
            "email": data["emailAddresses"][0]["value"],
            "first_name": data["names"][0]["givenName"],
            "last_name": data["names"][0]["familyName"],
            "company_name": (
                data["organizations"][0]["name"] if "organizations" in data else ""
            ),
            "job_title": (
                data["organizations"][0]["title"] if "organizations" in data else ""
            ),
        }

    def send_email(self, to, subject, message_text):
        if not self.email_address:
            user_info = self.get_user_info()
            self.email_address = user_info["email"]
        message = MIMEText(message_text)
        message["to"] = to
        message["from"] = self.email_address
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        message = {"raw": raw}
        response = requests.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(message),
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.post(
                "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(message),
            )
        return response.json()
