# Withings SSO Integration

This document provides detailed instructions on how to configure and use Withings Single Sign-On (SSO) for authenticating users and accessing user data using OAuth.

## Required Environment Variables

To set up Withings SSO, you need the following environment variables. Ensure you add these to your `.env` file.

- `WITHINGS_CLIENT_ID`: Withings OAuth client ID
- `WITHINGS_CLIENT_SECRET`: Withings OAuth client secret

### Steps to Acquire Withings Client ID and Secret

1. **Register your application with Withings**:
   - Visit the [Withings Developer Portal](https://developer.withings.com/).
   - Log in or sign up if you don't already have an account.
   - Create a new application under your account.
   - Fill in the required details such as application name, description, and redirect URIs.

2. **Generate the Client ID and Secret**:
   - Once your application is created, navigate to the application details page.
   - You will find the `Client ID` and `Client Secret` here. Copy these values to your `.env` file.

```plaintext
WITHINGS_CLIENT_ID=your_withings_client_id
WITHINGS_CLIENT_SECRET=your_withings_client_secret
```

## Required Scopes for Withings SSO

When configuring the Withings SSO, make sure to request the following scopes. These scopes ensure that your application has the necessary permissions to access user information and metrics.

- `user.info`: Access basic user information.
- `user.metrics`: Access user's health metrics.
- `user.activity`: Access user's activity data.

## WithingsSSO Class

The `WithingsSSO` class implements the core functionality for authenticating users and retrieving user information using Withings API.

### Methods

- **`__init__(self, access_token=None, refresh_token=None)`**: Initialize the class with access and refresh tokens.
- **`get_new_token(self)`**: Obtain a new access token using the refresh token.
- **`get_user_info(self)`**: Retrieve user information like first name, last name, and email.
- **`send_email(self, to, subject, message_text)`**: Method is not implemented as Withings API does not support sending emails.

### `withings_sso` Function

The `withings_sso` function handles the OAuth token exchange process and returns an instance of `WithingsSSO`.

- **Parameters**:
  - `code`: The authorization code received from Withings after user authorization.
  - `redirect_uri`: (Optional) The redirect URI registered with the Withings application.

- **Returns**:
  - An instance of `WithingsSSO` containing the access and refresh tokens.

### Code Example

Here's a basic example of how to use the `WithingsSSO` class and `withings_sso` function in your application:

```python
from withings import withings_sso

# Assume you have received an authorization code from Withings
authorization_code = "your_authorization_code"

# Perform the OAuth token exchange and get the WithingsSSO instance
withings_instance = withings_sso(authorization_code)

if withings_instance:
    user_info = withings_instance.user_info
    print("User email:", user_info["email"])
    print("First Name:", user_info["first_name"])
    print("Last Name:", user_info["last_name"])
else:
    print("Failed to authenticate with Withings.")
```

Add the above code to your script or application to authenticate users using Withings SSO and retrieve basic user information.

### Logging

This script includes basic error logging to help troubleshooting during the OAuth process. If there is a problem when exchanging tokens or retrieving user information, an error message will be logged.

## Conclusion

With this setup, you can easily integrate Withings SSO into your application to authenticate users and access their Withings data. Ensure you securely store your `WITHINGS_CLIENT_ID` and `WITHINGS_CLIENT_SECRET` in your environment variables.