# Huddle SSO

This module facilitates Single Sign-On (SSO) with Huddle and provides functionalities to retrieve user information and send emails via Huddle's API.

## Required Environment Variables

To utilize the Huddle SSO functionalities in this module, you need to set up the following environment variables in your `.env` file:

- `HUDDLE_CLIENT_ID`: Huddle OAuth client ID
- `HUDDLE_CLIENT_SECRET`: Huddle OAuth client secret

### How to Acquire the Required Keys

1. **Create a Huddle App:**
   - Visit the Huddle Developer Portal [Huddle Dev Portal](https://www.huddle.com/developers/).
   - Log in with your Huddle account.
   - Navigate to the 'Apps' section and create a new application.
   - Fill in the necessary details, including redirect URI and scopes.
   - Upon creation, you will be provided with a `Client ID` and a `Client Secret`.

2. **Add Keys to `.env` File:**
   - Open your `.env` file in the root of your project.
   - Add the following lines:
     ```
     HUDDLE_CLIENT_ID=your_client_id_here
     HUDDLE_CLIENT_SECRET=your_client_secret_here
     ```

## Required APIs

Ensure you have the necessary Huddle APIs enabled:

- Make sure your created application in the Huddle Developer Portal has permissions for the required scopes listed below.

## Required Scopes for Huddle OAuth

Generate access tokens with the following scopes:

- `user_info`
- `send_email`

## Example Usage

Here's how to use the HuddleSSO class and the `huddle_sso` function.

### Initializing Huddle SSO

First, create an instance of the `HuddleSSO` class.

```python
from huddle import HuddleSSO, huddle_sso

# Mock authorization code you obtained via Huddle OAuth
auth_code = "your_auth_code_here"
redirect_uri = "your_redirect_uri_here"

# Initialize the SSO object
sso_obj = huddle_sso(auth_code, redirect_uri)

if sso_obj:
    print("Access Token:", sso_obj.access_token)
    print("Refresh Token:", sso_obj.refresh_token)
    print("User Info:", sso_obj.user_info)
else:
    print("Error in obtaining Huddle SSO.")
```

### Fetching User Information

Fetch and print user information.

```python
user_info = sso_obj.get_user_info()
print("User Info:", user_info)
```

### Sending an Email

Send an email using Huddle's send_email API.

```python
to = "recipient@example.com"
subject = "Test Email Subject"
message_text = "This is a test email message."

response = sso_obj.send_email(to, subject, message_text)
print("Email Response:", response)
```

## Detailed Steps for OAuth Flow

1. **Redirect User to Huddle Authorization Prompt:**
   - Redirect your user to the Huddle authorization page with the required scopes (`user_info`, `send_email`).
   - Example authorization URL:
     ```
     https://login.huddle.com/oauth2/authorize?response_type=code&client_id=your_client_id_here&redirect_uri=your_redirect_uri_here&scope=user_info send_email
     ```

2. **Obtain Authorization Code:**
   - After the user authorizes your app, Huddle will redirect them to your specified redirect URI with an authorization code.

3. **Exchange Authorization Code for Access Token and Refresh Token:**
   - Use the `huddle_sso` function to exchange the authorization code for an access token and refresh token.
   - Example:
     ```python
     sso_obj = huddle_sso(auth_code, redirect_uri)
     ```

4. **Use Access Token for API Requests:**
   - With the access token, you can make authorized API requests to Huddle on behalf of the user.

## Error Handling

The provided methods include basic error handling with appropriate HTTP exceptions and logging. Make sure to handle exceptions in your implementation as needed.

By following these instructions, you should be able to set up and utilize Huddle SSO in your application effectively. If you encounter any issues, refer to the Huddle API documentation and ensure all provided client ID, client secret, and scopes are correctly configured.