# Basecamp SSO Integration Guide

This guide provides detailed instructions on setting up Basecamp Single Sign-On (SSO) in your application. By following this guide, you'll be able to seamlessly authenticate users using their Basecamp account.

## Prerequisites

Before you begin, ensure you have the following:

1. A [Basecamp](https://basecamp.com/) account.
2. The required environment variables:
   - `BASECAMP_CLIENT_ID`
   - `BASECAMP_CLIENT_SECRET`

## Setting Up Basecamp OAuth

1. **Register an OAuth Application**:
   - Go to the [Basecamp Developer Portal](https://integrate.37signals.com/) and create a new application.
   - Fill in the required details such as application name and redirect URI. The redirect URI will be used later in the integration process.
   - Upon creation, you will receive your `BASECAMP_CLIENT_ID` and `BASECAMP_CLIENT_SECRET`.

2. **Enable Required APIs**:
   - **Auth Code API**: This endpoint is used to obtain the authorization code.
     - URL: `https://launchpad.37signals.com/authorization/new`
   - **Token API**: This endpoint is used to exchange the authorization code for an access token.
     - URL: `https://launchpad.37signals.com/authorization/token`
   - **Users API**: This endpoint retrieves the authenticated user's information.
     - URL: `https://3.basecampapi.com/{account_id}/people/me.json`

3. **Add Environment Variables**:
   - Create a `.env` file in your project's root directory if it does not exist.
   - Add the following entries to the `.env` file:
     ```env
     BASECAMP_CLIENT_ID=your_basecamp_client_id
     BASECAMP_CLIENT_SECRET=your_basecamp_client_secret
     ```

## Code Overview

The following section provides an overview of the implementation code and its functionalities:

### Class: `BasecampSSO`

- **Attributes**:
  - `access_token`: The OAuth access token.
  - `refresh_token`: The OAuth refresh token.
  - `client_id`: Basecamp OAuth client ID.
  - `client_secret`: Basecamp OAuth client secret.
  - `account_id`: The ID of the authenticated user's Basecamp account.
  - `user_info`: A dictionary containing the user's information, such as email, first name, and last name.

- **Methods**:
  - `__init__(self, access_token=None, refresh_token=None, account_id=None)`: Initializes the access and refresh tokens, client credentials, and user information.
  - `get_new_token(self)`: Refreshes the access token using the refresh token.
  - `get_user_info(self)`: Retrieves the authenticated user's information from the Basecamp API.
  - `send_email(self, to, subject, message_text)`: Raises `NotImplementedError` since Basecamp does not have a native email API.

### Function: `basecamp_sso`

This function handles the OAuth flow to authenticate a user and obtain the access and refresh tokens.

- **Parameters**:
  - `code`: The authorization code received from the OAuth flow.
  - `redirect_uri`: The redirect URI registered with Basecamp (default is `MAGIC_LINK_URL` from the environment).

- **Returns**: An instance of `BasecampSSO` containing the authenticated user's access and refresh tokens and user information.

### Example Usage

Here's an example of how to use the `BasecampSSO` class in your application:

```python
from your_module_path import basecamp_sso

# Assume `code` is obtained from the OAuth flow
code = "your_authorization_code"

# Initialize Basecamp SSO
basecamp_sso_instance = basecamp_sso(code)

if basecamp_sso_instance:
    # Access user information
    user_info = basecamp_sso_instance.user_info
    print(f"User Email: {user_info['email']}")
    print(f"User Name: {user_info['first_name']} {user_info['last_name']}")
else:
    print("Error: Unable to authenticate user with Basecamp.")
```

## Conclusion

By following this guide, you should be able to set up and integrate Basecamp SSO into your application. Make sure to replace placeholder values with your actual Basecamp application credentials and handle the authorization code flow appropriately in your application to obtain the `code` parameter required for authentication.