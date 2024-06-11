import base64
import json
import requests
from email.mime.text import MIMEText
from Globals import getenv

"""
Required environment variables:

- GOOGLE_CLIENT_ID: Google OAuth client ID
- GOOGLE_CLIENT_SECRET: Google OAuth client secret

Get the Google OAuth client ID and client secret from the Google Cloud Console.

Required APIs:

- People API
- Gmail API

Required scopes for Google SSO:
- https://www.googleapis.com/auth/userinfo.profile
- https://www.googleapis.com/auth/gmail.send
"""


class GoogleSSO:
    def __init__(
        self,
        access_token,  # Comes from Google OAuth and stored in db
        refresh_token,  # Comes from Google OAuth and stored in db
    ):
        self.refresh_token = refresh_token
        self.access_token = access_token
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
                "https://people.googleapis.com/v1/people/me",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        data = response.json()
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