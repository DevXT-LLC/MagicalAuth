## ClearScore Single Sign-On (SSO) Integration Documentation

This document details how to integrate ClearScore SSO into your application. It includes setup steps, environment variable configurations, and API requirements.

### Required Environment Variables

To use ClearScore SSO, you need to configure the following environment variables in your `.env` file:

- `CLEAR_SCORE_CLIENT_ID`: ClearScore OAuth client ID
- `CLEAR_SCORE_CLIENT_SECRET`: ClearScore OAuth client secret

### Acquiring ClearScore OAuth Credentials

1. **Register Your Application**: Visit the ClearScore API developer portal and register your application.
2. **Obtain Client Credentials**: After registration, you will receive a `Client ID` and `Client Secret`.
3. **Set Environment Variables**: Add the `CLEAR_SCORE_CLIENT_ID` and `CLEAR_SCORE_CLIENT_SECRET` values to your `.env` file in the following format:

```plaintext
CLEAR_SCORE_CLIENT_ID=your_clear_score_client_id
CLEAR_SCORE_CLIENT_SECRET=your_clear_score_client_secret
```

### Required APIs

To interact with ClearScore's OAuth and email sending capabilities, ensure your application requests the following scopes:

- `user.info.read`
- `email.send`

### Scope Descriptions

- **`user.info.read`**: Allows reading of user profile information.
- **`email.send`**: Allows sending emails on behalf of the user.

### ClearScore Integration Code

The provided Python code establishes an SSO class `ClearScoreSSO` which handles authentication and email functionalities for ClearScore.

#### Class: `ClearScoreSSO`

- **Properties**:
  - `access_token`: The OAuth access token required to make authenticated requests.
  - `refresh_token`: The OAuth refresh token used to obtain a new access token.
  - `client_id`: OAuth client ID from environment.
  - `client_secret`: OAuth client secret from environment.
  - `user_info`: User's profile information.

- **Methods**:
  - `__init__(self, access_token=None, refresh_token=None)`: Constructor that initializes the instance with tokens and obtains user info.
  - `get_new_token()`: Requests a new access token using the refresh token.
  - `get_user_info()`: Fetches and returns the user's profile information.
  - `send_email(to, subject, message_text)`: Sends an email to the specified recipient using ClearScore email API.

#### Function: `clearscore_sso(code, redirect_uri=None) -> ClearScoreSSO`

This function exchanges the authorization code for an access token and returns an instance of `ClearScoreSSO`.

##### Parameters:

- `code`: The authorization code returned by ClearScore.
- `redirect_uri`: The redirect URI registered with ClearScore.

### Usage Example

Below is an example demonstrating how to initiate a ClearScore SSO session and send an email.

```python
from your_module_path import clearscore_sso

# Replace 'your_code' with the actual authorization code from ClearScore
code = "your_code"
redirect_uri = "your_registered_redirect_uri"

# Obtain an instance of ClearScoreSSO
clearscore_instance, error = clearscore_sso(code, redirect_uri)

if error is None:
    # Send an email using the ClearScoreSSO instance
    email_sent = clearscore_instance.send_email(
        to="recipient@example.com",
        subject="Test Email",
        message_text="This is a test email from ClearScore SSO."
    )

    if email_sent:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")
else:
    print(f"Failed to obtain ClearScore SSO instance: {error}")
```

### Error Handling

The code includes error handling to manage token refresh and API request failures. If an error occurs while refreshing tokens or fetching user info, an `HTTPException` will be raised with the appropriate status code and error message.

### Summary

By following the steps above and using the provided code, you can integrate ClearScore SSO into your application to authenticate users and send emails securely. Ensure you have all the required environment variables and API scopes properly configured for a seamless experience.