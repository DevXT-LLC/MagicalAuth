# Okta SSO Setup and Usage

This section provides detailed documentation on setting up and using Okta Single Sign-On (SSO) in your project. By following these steps, you will be able to authenticate users using Okta and retrieve their user information.

## Required Environment Variables

Before you begin, ensure you have the following environment variables set up in your `.env` file:

- `OKTA_CLIENT_ID`: Okta OAuth client ID
- `OKTA_CLIENT_SECRET`: Okta OAuth client secret
- `OKTA_DOMAIN`: Okta domain (e.g., dev-123456.okta.com)

## Required OAuth Scopes

Ensure that your Okta OAuth application has the following scopes enabled:

- `openid`
- `profile`
- `email`

## Setting Up

### Step 1: Creating an Okta Application

1. Log in to your Okta Developer account at [developer.okta.com](https://developer.okta.com/).
2. From the dashboard, navigate to **Applications** -> **Applications**.
3. Click on **Create App Integration**.
4. Select **OAuth 2.0 / OIDC**, then click **Next**.
5. Choose **Web Application** and configure the following settings:
    - **Sign-in redirect URIs**: Add the callback URI of your application (e.g., `http://localhost:8000/callback`)
    - **Sign-out redirect URIs**: Optionally, add a sign-out URI.
6. Click **Save**.

### Step 2: Retrieving Your Okta Client ID and Client Secret

1. After saving the application, you will be redirected to the application settings page.
2. Scroll down to the **Client Credentials** section.
3. Copy the **Client ID** and **Client Secret** and add them to your `.env` file:
    ```plaintext
    OKTA_CLIENT_ID=your_client_id
    OKTA_CLIENT_SECRET=your_client_secret
    ```

### Step 3: Configuring Your Okta Domain

1. In the Okta dashboard, navigate to **Settings** -> **Customizations** -> **Domain**.
2. Copy your Okta domain (e.g., `dev-123456.okta.com`) and add it to your `.env` file:
    ```plaintext
    OKTA_DOMAIN=your_okta_domain
    ```

### Step 4: Configuring Your Project

Ensure that your project is set up to read environment variables. One popular way to achieve this is by using the `python-dotenv` library. Install it using pip if you haven't already:

```bash
pip install python-dotenv
```

In your project, ensure that you load the environment variables at the start:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file
```

## Usage

### Instantiating OktaSSO Class

To authenticate a user and retrieve their information, you can use the `okta_sso` function and the `OktaSSO` class as follows:

```python
from sso.okta import okta_sso

# Assuming you have obtained an authorization code from Okta
authorization_code = "<your_authorization_code>"

# Optionally, set a custom redirect URI (if different from the one configured in Okta)
redirect_uri = "http://localhost:8000/callback"

# Authenticate and retrieve OktaSSO instance
okta_sso_instance = okta_sso(authorization_code, redirect_uri)

if okta_sso_instance:
    user_info = okta_sso_instance.user_info
    print(f"User email: {user_info['email']}")
    print(f"First name: {user_info['first_name']}")
    print(f"Last name: {user_info['last_name']}")
else:
    print("Authentication failed.")
```

### Refreshing Access Token

The `OktaSSO` class provides a method to refresh the access token using the refresh token:

```python
okta_sso_instance = OktaSSO(access_token="<access_token>", refresh_token="<refresh_token>")
new_access_token = okta_sso_instance.get_new_token()
print(f"New Access Token: {new_access_token}")
```

### Sending Emails (Not Implemented)

The `send_email` method in the `OktaSSO` class is a placeholder and currently not implemented. You may need additional integrations to send emails using Okta or another service provider.

```python
try:
    okta_sso_instance.send_email(to="user@example.com", subject="Test", message_text="This is a test.")
except NotImplementedError as e:
    print(e)
```

By following these steps and references, you should have a functional Okta SSO integration in your project. Ensure all necessary configurations and environment variables are correctly set to avoid any issues.