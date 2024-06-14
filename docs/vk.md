# VK SSO

## Required Environment Variables

- `VK_CLIENT_ID`: VK OAuth client ID
- `VK_CLIENT_SECRET`: VK OAuth client secret

## Required APIs

Ensure that you have the necessary VK APIs enabled by following these instructions. Once confirmed, add the `VK_CLIENT_ID` and `VK_CLIENT_SECRET` environment variables to your `.env` file.

1. **VK API Access Setup:**
   - Visit VK's [Developers Page](https://vk.com/dev) and create a new application if you haven't done so already.
   - Note down the Application ID (this will be your VK Client ID) and secure your Application Secret (this will be your VK Client Secret).
   - Configure your application to use VK API.

2. **Get the VK Client ID and Client Secret:**
   - After setting up your VK application, go to the application settings.
   - From the application settings, retrieve the **Application ID** which will serve as `VK_CLIENT_ID`.
   - Retrieve the **Secure Key** which will serve as `VK_CLIENT_SECRET`.

Add these values to your `.env` file in the following format:

```
VK_CLIENT_ID=your_vk_client_id
VK_CLIENT_SECRET=your_vk_client_secret
```

## Required Scopes for VK SSO

To authenticate users via VK SSO, you need the following scope:

- `email`

Make sure your VK application requests this scope during the OAuth authorization process.

## Authentication Flow

Here is a basic outline of the VK SSO authentication flow implemented in the provided code:

1. **OAuth Redirect:**
   - Redirect the user to VK's OAuth authorization URL with your `VK_CLIENT_ID`, desired scopes, and a `redirect_uri`.

2. **Authorization Code:**
   - After the user authorizes the app, VK redirects them back to your specified `redirect_uri` with a `code` (Authorization Code).

3. **Exchange Code for Access Token:**
   - Exchange this `code` for an `access_token` by making a request to VK's `https://oauth.vk.com/access_token` endpoint.
  
4. **Fetch User Info:**
   - Use the `access_token` to query VK's `https://api.vk.com/method/users.get` endpoint to retrieve user information (first name, last name) using the user ID. The code below handles this process and raises appropriate HTTP exceptions if any API calls fail.

```python
import requests
import logging
from fastapi import HTTPException
from Globals import getenv

class VKSSO:
    def __init__(
        self,
        access_token=None,
        user_id=None,
        email=None,
    ):
        self.access_token = access_token
        self.user_id = user_id
        self.email = email
        self.client_id = getenv("VK_CLIENT_ID")
        self.client_secret = getenv("VK_CLIENT_SECRET")
        self.user_info = self.get_user_info()

    def get_new_token(self):
        raise NotImplementedError("VK API does not use refresh tokens.")

    def get_user_info(self):
        uri = f"https://api.vk.com/method/users.get?user_ids={self.user_id}&fields=first_name,last_name&access_token={self.access_token}&v=5.131"
        response = requests.get(uri)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error getting user info from VK",
            )
        try:
            data = response.json()["response"][0]
            first_name = data["first_name"]
            last_name = data["last_name"]
            return {
                "email": self.email,
                "first_name": first_name,
                "last_name": last_name,
            }
        except:
            raise HTTPException(
                status_code=400,
                detail="Error parsing user info from VK",
            )

    def send_email(self, to, subject, message_text):
        raise NotImplementedError("VK API does not support sending emails.")

def vk_sso(code, redirect_uri=None) -> VKSSO:
    if not redirect_uri:
        redirect_uri = getenv("MAGIC_LINK_URL")
    response = requests.get(
        "https://oauth.vk.com/access_token",
        params={
            "client_id": getenv("VK_CLIENT_ID"),
            "client_secret": getenv("VK_CLIENT_SECRET"),
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    if response.status_code != 200:
        logging.error(f"Error getting VK access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    user_id = data["user_id"]
    email = data.get("email", "Not provided")
    return VKSSO(access_token=access_token, user_id=user_id, email=email)
```