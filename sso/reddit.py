import base64
import json
import requests
import logging
from email.mime.text import MIMEText
from fastapi import HTTPException
from Globals import getenv

"""
Required environment variables:

- REDDIT_CLIENT_ID: Reddit OAuth client ID
- REDDIT_CLIENT_SECRET: Reddit OAuth client secret

Required APIs

Follow the links to confirm that you have the APIs enabled,
then add the `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` environment variables to your `.env` file.

Required scopes for Reddit OAuth

- identity
- submit
- read
"""


class RedditSSO:
    def __init__(
        self,
        access_token=None,
        refresh_token=None,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = getenv("REDDIT_CLIENT_ID")
        self.client_secret = getenv("REDDIT_CLIENT_SECRET")
        self.user_info = self.get_user_info()

    def get_new_token(self):
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=(self.client_id, self.client_secret),
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
            headers={"User-Agent": "MyRedditApp"}
        )
        return response.json()["access_token"]

    def get_user_info(self):
        uri = "https://oauth.reddit.com/api/v1/me"
        response = requests.get(
            uri,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": "MyRedditApp"
            },
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.get(
                uri,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "User-Agent": "MyRedditApp"
                },
            )
        try:
            data = response.json()
            username = data['name']
            email = data.get('email', '')
            # Reddit API does not inherently provide first_name and last_name
            return {
                "email": email,
                "username": username,
            }
        except:
            raise HTTPException(
                status_code=400,
                detail="Error getting user info from Reddit",
            )

    def submit_post(self, subreddit, title, content):
        post_data = {
            "sr": subreddit,
            "title": title,
            "text": content,
            "kind": "self"
        }
        response = requests.post(
            "https://oauth.reddit.com/api/submit",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": "MyRedditApp",
                "Content-Type": "application/json",
            },
            data=json.dumps(post_data),
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.post(
                "https://oauth.reddit.com/api/submit",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "User-Agent": "MyRedditApp",
                    "Content-Type": "application/json",
                },
                data=json.dumps(post_data),
            )
        if response.status_code != 200:
            logging.error(f"Error submitting post to Reddit: {response.text}")
        return response.json()


def reddit_sso(code, redirect_uri=None) -> RedditSSO:
    if not redirect_uri:
        redirect_uri = getenv("MAGIC_LINK_URL")
    code = (
        str(code)
        .replace("%2F", "/")
        .replace("%3D", "=")
        .replace("%3F", "?")
        .replace("%26", "&")
    )
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=(getenv("REDDIT_CLIENT_ID"), getenv("REDDIT_CLIENT_SECRET")),
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        },
        headers={"User-Agent": "MyRedditApp"}
    )
    if response.status_code != 200:
        logging.error(f"Error getting Reddit access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    return RedditSSO(access_token=access_token, refresh_token=refresh_token)
