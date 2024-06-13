import requests
import logging
from fastapi import HTTPException
from Globals import getenv

"""
Required environment variables:

- BASECAMP_CLIENT_ID: Basecamp OAuth client ID
- BASECAMP_CLIENT_SECRET: Basecamp OAuth client secret

Required APIs and Scopes for Basecamp SSO

- Auth Code https://launchpad.37signals.com/authorization/new
- Token   https://launchpad.37signals.com/authorization/token
- Users API: https://3.basecampapi.com/{account_id}/people/me.json
- Email API: (Basecamp does not have a native email API, this would likely need to be 
             handled through integration with another email service)

Follow the links to ensure you have the APIs enabled and add the 
`BASECAMP_CLIENT_ID` and `BASECAMP_CLIENT_SECRET` environment variables to your `.env` file.
"""


class BasecampSSO:
    def __init__(self, access_token=None, refresh_token=None, account_id=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = getenv("BASECAMP_CLIENT_ID")
        self.client_secret = getenv("BASECAMP_CLIENT_SECRET")
        self.account_id = account_id
        self.user_info = self.get_user_info()

    def get_new_token(self):
        response = requests.post(
            "https://launchpad.37signals.com/authorization/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "type": "refresh",
            },
        )
        return response.json()["access_token"]

    def get_user_info(self):
        uri = f"https://3.basecampapi.com/{self.account_id}/people/me.json"
        response = requests.get(
            uri,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.get(
                uri,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        try:
            data = response.json()
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email_address"]
            return {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        except:
            raise HTTPException(
                status_code=400,
                detail="Error getting user info from Basecamp",
            )

    def send_email(self, to, subject, message_text):
        raise NotImplementedError("Basecamp does not support a native email API")


def basecamp_sso(code, redirect_uri=None) -> BasecampSSO:
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
        f"https://launchpad.37signals.com/authorization/token",
        data={
            "client_id": getenv("BASECAMP_CLIENT_ID"),
            "client_secret": getenv("BASECAMP_CLIENT_SECRET"),
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
    )
    if response.status_code != 200:
        logging.error(f"Error getting Basecamp access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    account_id = data["accounts"][0]["id"]
    return BasecampSSO(
        access_token=access_token, refresh_token=refresh_token, account_id=account_id
    )
