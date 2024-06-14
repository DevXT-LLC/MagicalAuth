## Bitbucket SSO Integration

The `BitbucketSSO` class facilitates Single Sign-On (SSO) via Bitbucket. This integration enables your application to authenticate users with their Bitbucket accounts, providing an easy way for users to log in without creating a new account on your platform.

### Required Environment Variables

To set up Bitbucket SSO, you need to obtain and set the following environment variables:

- `BITBUCKET_CLIENT_ID`: Bitbucket OAuth client ID
- `BITBUCKET_CLIENT_SECRET`: Bitbucket OAuth client secret

### Step-by-Step Guide

#### 1. Register Your Application on Bitbucket

1. Visit the Bitbucket developer portal: [Bitbucket OAuth Settings](https://bitbucket.org/account/settings/app-passwords/).
2. Log in with your Bitbucket account.
3. Navigate to "OAuth" under "Access Management."
4. Click on "Add consumer."
5. Fill in the required details:
    - **Name**: A name for your application.
    - **Description**: A brief description of what the application does.
    - **Callback URL**: The URL to which Bitbucket will send users after they authorize.
6. Select the necessary scopes for your application. For Bitbucket SSO, you need at least:
    - `account`
    - `email`
7. Save the consumer to get the Client ID and Client Secret.

#### 2. Set Environment Variables

Add the obtained credentials to your `.env` file:

```
BITBUCKET_CLIENT_ID=your_bitbucket_client_id
BITBUCKET_CLIENT_SECRET=your_bitbucket_client_secret
```

#### 3. Required Scopes for Bitbucket SSO

Ensure that you request the following scopes when redirecting users for authentication:

- `account`
- `email`

### How To Use

#### BitbucketSSO Class

The `BitbucketSSO` class handles the retrieval of user information using access and refresh tokens.

```python
from sso.bitbucket import BitbucketSSO

def bitbucket_login(auth_code, redirect_uri):
    bitbucket_user = bitbucket_sso(auth_code, redirect_uri)
    if not bitbucket_user:
        raise Exception("Authentication failed.")
    user_info = bitbucket_user.user_info
    email = user_info.get("email")
    first_name = user_info.get("first_name")
    last_name = user_info.get("last_name")
    # Use this information as needed in your application.
```

#### Functions and Methods

1. **Constructor (`__init__`)**

    Initializes the `BitbucketSSO` object with the provided tokens and retrieves the user's info.

    ```python
    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = getenv("BITBUCKET_CLIENT_ID")
        self.client_secret = getenv("BITBUCKET_CLIENT_SECRET")
        self.user_info = self.get_user_info()
    ```

2. **Get New Token (`get_new_token`)**

    Refreshes the access token using the refresh token.

    ```python
    def get_new_token(self):
        # Implementation...
    ```

3. **Get User Info (`get_user_info`)**

    Retrieves user information from Bitbucket.

    ```python
    def get_user_info(self):
        # Implementation...
    ```

4. **Bitbucket SSO Function (`bitbucket_sso`)**

    Exchanges the authorization code for access and refresh tokens and returns an instance of `BitbucketSSO`.

    ```python
    def bitbucket_sso(code, redirect_uri=None) -> BitbucketSSO:
        # Implementation...
    ```

### Example Usage

```python
from sso.bitbucket import bitbucket_sso

# Assuming `auth_code` is obtained from the OAuth callback and `redirect_uri` is configured
bitbucket_user = bitbucket_sso(auth_code, redirect_uri)
user_info = bitbucket_user.user_info
print(f"User's email is: {user_info['email']}")
```

By following this setup, you should be able to integrate Bitbucket SSO into your application seamlessly. If you encounter any issues, double-check your environment variable setup and ensure that your OAuth consumer is configured correctly on the Bitbucket developer portal.