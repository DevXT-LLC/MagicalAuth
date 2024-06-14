# Cloud Foundry Single Sign-On (SSO) Integration

This document describes how to set up and use Cloud Foundry SSO in your application. Follow the steps below to configure the integration, acquire the necessary keys, and set up your environment.

## Required Environment Variables

- `CF_CLIENT_ID`: Cloud Foundry OAuth client ID
- `CF_CLIENT_SECRET`: Cloud Foundry OAuth client secret

## Required APIs and Scopes

You need to enable the following APIs and ensure the appropriate scopes are configured.

- **Cloud Foundry API (CF API)**
- **User Info API**

### Steps to Acquire Required Keys

1. **Log in to your Cloud Foundry Account:**  
   Go to your Cloud Foundry provider’s management console and log in using your credentials.

2. **Register an Application:**  
   Navigate to the OAuth Applications section. Create a new OAuth application.

3. **Obtain Client ID and Client Secret:**  
   Once the application is created, you will receive a `CLIENT_ID` and `CLIENT_SECRET`. Make a note of these values as you will need to set them as environment variables.

4. **Set up Redirect URIs:**  
   Specify the redirect URIs required for your application. These should point to the appropriate endpoints in your application handling OAuth redirects.

5. **Enable CF OAuth and User Info API:**  
   Ensure that the Cloud Foundry OAuth and User Info APIs are enabled for your account or organization. This often involves checking specific settings in the Cloud Foundry management console.

## Required Scopes for Cloud Foundry SSO

Ensure that the following OAuth scopes are included in your application's authorization request:

- `openid`
- `profile`
- `email`

## Setting Up Environment Variables

After acquiring the necessary credentials, set up your environment variables. Add the following lines to your application's `.env` file:

```
CF_CLIENT_ID=YOUR_CLOUD_FOUNDRY_CLIENT_ID
CF_CLIENT_SECRET=YOUR_CLOUD_FOUNDRY_CLIENT_SECRET
MAGIC_LINK_URL=YOUR_APPLICATION_REDIRECT_URI
```

Replace `YOUR_CLOUD_FOUNDRY_CLIENT_ID`, `YOUR_CLOUD_FOUNDRY_CLIENT_SECRET`, and `YOUR_APPLICATION_REDIRECT_URI` with the actual values you obtained during the setup process.

## Implementation

Here’s an overview of the Cloud Foundry SSO integration implementation:

```python
# ./sso/cloud_foundry.py
import requests
import logging
from fastapi import HTTPException
from Globals import getenv

class CloudFoundrySSO:
    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = getenv("CF_CLIENT_ID")
        self.client_secret = getenv("CF_CLIENT_SECRET")
        self.user_info = self.get_user_info()

    def get_new_token(self):
        response = requests.post(
            "https://login.system.example.com/oauth/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            },
        )
        return response.json()["access_token"]

    def get_user_info(self):
        uri = "https://uaa.system.example.com/userinfo"
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
            first_name = data["given_name"]
            last_name = data["family_name"]
            email = data["email"]
            return {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        except:
            raise HTTPException(
                status_code=400,
                detail="Error getting user info from Cloud Foundry",
            )

    def send_email(self, to, subject, message_text):
        raise NotImplementedError(
            "Email sending not supported for Cloud Foundry SSO yet."
        )

def cloud_foundry_sso(code, redirect_uri=None) -> CloudFoundrySSO:
    if not redirect_uri:
        redirect_uri = getenv("MAGIC_LINK_URL")
    code = (
        str(code)
        .replace("%2F", "/")
        .replace("%3D", "=")
        .replace("%3A", ":")
        .replace("%3F", "?")
    )
    response = requests.post(
        "https://login.system.example.com/oauth/token",
        data={
            "client_id": getenv("CF_CLIENT_ID"),
            "client_secret": getenv("CF_CLIENT_SECRET"),
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
    )
    if response.status_code != 200:
        logging.error(f"Error getting Cloud Foundry access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    return CloudFoundrySSO(access_token=access_token, refresh_token=refresh_token)
```

### Dependencies

Ensure you have the following dependencies installed in your environment:

- `fastapi`
- `requests`

You can install them using pip:

```bash
pip install fastapi requests
```

With this documentation and the provided implementation, you should be able to set up and integrate Cloud Foundry SSO into your application seamlessly. If you run into any issues, please refer to the Cloud Foundry documentation or reach out to their support for further assistance.