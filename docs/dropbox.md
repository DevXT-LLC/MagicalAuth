## Dropbox SSO Integration

This document describes how to integrate Dropbox Single Sign-On (SSO) with your application. By following these instructions, you will be able to allow users to authenticate with Dropbox and access their Dropbox account information and files.

### Required Environment Variables

Before you start, you need to obtain the necessary credentials and set up environment variables:

1. **DROPBOX_CLIENT_ID**: Your Dropbox OAuth client ID.
2. **DROPBOX_CLIENT_SECRET**: Your Dropbox OAuth client secret.

### Acquiring Dropbox OAuth Credentials

To obtain the necessary credentials from Dropbox:

1. **Create a Dropbox App**:
    - Visit the [Dropbox App Console](https://www.dropbox.com/developers/apps).
    - Click on "Create App".
    - Choose an API (Scoped access).
    - Select the type of access you need: "Full Dropbox" or "App Folder".
    - Name your app and click "Create App".

2. **Get Your App Credentials**:
   - Navigate to the "Settings" tab of your app in the Dropbox App Console.
   - You will find your `App key` (use this as `DROPBOX_CLIENT_ID`) and `App secret` (use this as `DROPBOX_CLIENT_SECRET`).

3. **Set the Redirect URI**:
   - In the "OAuth 2" section in the settings tab, add your redirect URI (e.g., `https://yourapp.com/auth/dropbox/callback`).

### Required Scopes for Dropbox OAuth

When setting up OAuth access, ensure that you enable the following scopes:

- `account_info.read`: Required to access user account information.
- `files.metadata.read`: Required to read the metadata for files in the user's Dropbox.

### Setting Environment Variables

Add the following environment variables to your `.env` file:

```
DROPBOX_CLIENT_ID=your_dropbox_client_id
DROPBOX_CLIENT_SECRET=your_dropbox_client_secret
```

### Dropbox SSO Implementation

The following code demonstrates a Dropbox SSO implementation using FastAPI and the Dropbox SDK. Users can authenticate with Dropbox, and your application can access their Dropbox account information and list their files.

#### Example `dropbox.py` File

```python
import json
import requests
import logging
from fastapi import HTTPException
from Globals import getenv

class DropboxSSO:
    def __init__(
        self,
        access_token=None,
        refresh_token=None,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = getenv("DROPBOX_CLIENT_ID")
        self.client_secret = getenv("DROPBOX_CLIENT_SECRET")
        self.user_info = self.get_user_info()

    def get_new_token(self):
        response = requests.post(
            "https://api.dropboxapi.com/oauth2/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            },
        )
        return response.json()["access_token"]

    def get_user_info(self):
        uri = "https://api.dropboxapi.com/2/users/get_current_account"
        response = requests.post(
            uri,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.post(
                uri,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        try:
            data = response.json()
            first_name = data["name"]["given_name"]
            last_name = data["name"]["surname"]
            email = data["email"]
            return {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error getting user info from Dropbox: {e}",
            )

    def list_files(self):
        uri = "https://api.dropboxapi.com/2/files/list_folder"
        data = {
            "path": "",
            "recursive": False,
            "include_media_info": False,
            "include_deleted": False,
            "include_has_explicit_shared_members": False,
            "include_mounted_folders": True,
            "include_non_downloadable_files": True,
        }
        response = requests.post(
            uri,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.post(
                uri,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(data),
            )
        if response.status_code != 200:
            logging.error(f"Error listing files from Dropbox: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Error listing files from Dropbox",
            )
        return response.json()


def dropbox_sso(code, redirect_uri=None) -> DropboxSSO:
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
        f"https://api.dropboxapi.com/oauth2/token",
        data={
            "code": code,
            "client_id": getenv("DROPBOX_CLIENT_ID"),
            "client_secret": getenv("DROPBOX_CLIENT_SECRET"),
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    if response.status_code != 200:
        logging.error(f"Error getting Dropbox access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data.get("refresh_token", "")
    return DropboxSSO(access_token=access_token, refresh_token=refresh_token)
```

### Summary

- First, obtain your Dropbox OAuth credentials by creating an app on the [Dropbox App Console](https://www.dropbox.com/developers/apps).
- Next, set the required environment variables (`DROPBOX_CLIENT_ID` and `DROPBOX_CLIENT_SECRET`) in your `.env` file.
- Ensure that you have enabled the appropriate OAuth scopes (`account_info.read` and `files.metadata.read`).
- Implement the provided Python class to facilitate Dropbox SSO features in your application.

By following these steps, you will be able to integrate Dropbox SSO into your application, allowing users to authenticate via Dropbox and granting your application access to Dropbox resources like user account information and file listings.