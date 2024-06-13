import base64
import json
import requests
import logging
from email.mime.text import MIMEText
from fastapi import HTTPException
from Globals import getenv
from boxsdk import OAuth2, Client

"""
Required environment variables:

- BOX_CLIENT_ID: Box OAuth client ID
- BOX_CLIENT_SECRET: Box OAuth client secret

Required APIs

Ensure that you have the following Box APIs enabled,
then add the `BOX_CLIENT_ID` and `BOX_CLIENT_SECRET` environment variables to your `.env` file.

Required scopes for Box OAuth

- root_readwrite
- manage_app_users
"""


class BoxSSO:
    def __init__(
        self,
        access_token=None,
        refresh_token=None,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = getenv("BOX_CLIENT_ID")
        self.client_secret = getenv("BOX_CLIENT_SECRET")
        # Initialize Box OAuth2 with given tokens
        self.oauth2 = OAuth2(
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            store_tokens=self._store_tokens,
        )
        self.client = Client(self.oauth2)
        self.user_info = self.get_user_info()

    def _store_tokens(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_new_token(self):
        new_tokens = self.oauth2.refresh(self.refresh_token)
        self.access_token = new_tokens.access_token
        self.refresh_token = new_tokens.refresh_token
        return self.access_token

    def get_user_info(self):
        try:
            user = self.client.user().get()
            email = user.login
            first_name = user.name.split()[0]
            last_name = user.name.split()[-1]
            return {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        except Exception as e:
            logging.error(f"Error getting user info from Box: {e}")
            raise HTTPException(
                status_code=400,
                detail="Error getting user info from Box",
            )
    
    def send_email(self, to, subject, message_text):
        # Note: Box does not natively support sending emails as a service.
        # This function can be redefined to match any other communication needs with Box.
        raise NotImplementedError("Box does not support sending emails directly.")

def box_sso(code, redirect_uri=None) -> BoxSSO:
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
        f"https://api.box.com/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "client_id": getenv("BOX_CLIENT_ID"),
            "client_secret": getenv("BOX_CLIENT_SECRET"),
            "code": code,
            "redirect_uri": redirect_uri,
        },
    )
    if response.status_code != 200:
        logging.error(f"Error getting Box access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    return BoxSSO(access_token=access_token, refresh_token=refresh_token)
