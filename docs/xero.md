# Xero SSO Integration Documentation

## Overview

This document describes how to integrate Xero Single Sign-On (SSO) using the provided `xero.py` script. The script leverages Xero's OAuth 2.0 for authentication and retrieving user information.

## Prerequisites

1. **Create a Xero App**:
   
   To start using Xero's SSO, you need to create an app in the Xero Developer portal:
   - Go to the [Xero Developer Portal](https://developer.xero.com/myapps).
   - Sign in with your Xero account.
   - Click on "New App" and fill in the necessary details.
     - Application name: Provide a name for your application.
     - Integration: Select the type of integration (e.g., Web application).
     - OAuth 2.0 redirect URI: Provide your application's redirect URL.
   - Once the app is created, you will get the `CLIENT_ID` and `CLIENT_SECRET`. These are necessary for the OAuth flow.

2. **Environment Variables**:

   The keys fetched from the Xero Developer Portal need to be saved as environment variables in your project.

   - `XERO_CLIENT_ID`: Xero OAuth client ID
   - `XERO_CLIENT_SECRET`: Xero OAuth client secret

   Add these to your `.env` file:
   ```plaintext
   XERO_CLIENT_ID=your_client_id_here
   XERO_CLIENT_SECRET=your_client_secret_here
   MAGIC_LINK_URL=https://your-redirect-uri-here
   ```

## Usage

### Example Code Snippet

Below is a detailed breakdown of the `xero.py` script:

```python
import requests
import logging
from fastapi import HTTPException
from Globals import getenv

class XeroSSO:
    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = getenv("XERO_CLIENT_ID")
        self.client_secret = getenv("XERO_CLIENT_SECRET")
        self.user_info = self.get_user_info()
    
    def get_new_token(self):
        response = requests.post(
            "https://identity.xero.com/connect/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            },
        )
        if response.status_code != 200:
            logging.error(f"Error refreshing Xero token: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Unable to refresh token from Xero",
            )
        return response.json()["access_token"]
    
    def get_user_info(self):
        uri = "https://api.xero.com/connections"
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
            data = response.json()[0]  # Assuming you want the first connection info
            first_name = data.get("name", "").split()[0]
            last_name = " ".join(data.get("name", "").split()[1:])
            email = data.get("email", "")
            return {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        except Exception as exc:
            logging.error(f"Error parsing user info from Xero: {exc}")
            raise HTTPException(
                status_code=400,
                detail="Error getting user info from Xero",
            )
    
    def send_email(self, to, subject, message_text):
        # Xero does not provide an email sending service.
        raise NotImplementedError("Xero does not support sending emails via API.")

def xero_sso(code, redirect_uri=None) -> XeroSSO:
    if not redirect_uri:
        redirect_uri = getenv("MAGIC_LINK_URL")
    response = requests.post(
        "https://identity.xero.com/connect/token",
        data={
            "client_id": getenv("XERO_CLIENT_ID"),
            "client_secret": getenv("XERO_CLIENT_SECRET"),
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if response.status_code != 200:
        logging.error(f"Error getting Xero access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    return XeroSSO(access_token=access_token, refresh_token=refresh_token)
```

### Steps to Use the Script

1. **Setup Environment Variables**:
   
   Ensure you have the `.env` file in your project’s root directory with the following variables:

   ```plaintext
   XERO_CLIENT_ID=your_client_id_here
   XERO_CLIENT_SECRET=your_client_secret_here
   MAGIC_LINK_URL=https://your-redirect-uri-here
   ```

2. **Initialize OAuth Flow**:
   
   Use the `xero_sso` function to start the Xero OAuth process. You need to provide the authorization `code` obtained from the Xero OAuth callback.

   Example:
   ```python
   from your_module import xero_sso  # Replace 'your_module' with the actual module name

   code = "authorization_code_from_xero"
   xero_instance = xero_sso(code=code)

   # Access user info
   if xero_instance:
       print(xero_instance.user_info)
   else:
       print("Failed to authenticate with Xero")
   ```

3. **Handle User Information**:

   After successful authentication, the `XeroSSO` instance will contain the user’s information. You can access it via `xero_instance.user_info`.

## Error Handling

- If the OAuth token refresh fails, a detailed error will be logged, and an `HTTPException` will be raised.
- If there is an error while fetching the user's information, it will be logged, and an `HTTPException` will be raised.

## Limitations

- The script does not support sending emails via Xero's API as Xero does not provide an email sending service.
   
## Conclusion

By following the steps outlined in this documentation, you should be able to integrate Xero SSO into your application efficiently. Ensure that you have all the necessary environment variables correctly set up and that you handle errors gracefully in your implementation.