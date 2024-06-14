## Xing

The provided module allows for Single Sign-On (SSO) with Xing and includes the functionality to retrieve user information as well as send emails. Follow the steps below to set up and use the Xing SSO module.

### Required Environment Variables

To use the Xing SSO module, you need to set up two environment variables:

- `XING_CLIENT_ID`: Your Xing OAuth client ID
- `XING_CLIENT_SECRET`: Your Xing OAuth client secret

### Acquiring Environment Variables

1. **Xing OAuth Client ID and Client Secret**:
    - You will first need to create an application on [Xing Developer Portal](https://dev.xing.com/). Here’s how:
      1. Sign up or log into the [Xing Developer Portal](https://dev.xing.com/).
      2. Create a new application (you might have to complete some verification steps).
      3. Once your application is created, you will get access to the client ID and client secret.

2. **Setting Up Environment Variables**:
    - Add the `XING_CLIENT_ID` and `XING_CLIENT_SECRET` to your `.env` file:
      ```
      XING_CLIENT_ID=your_xing_oauth_client_id
      XING_CLIENT_SECRET=your_xing_oauth_client_secret
      ```

### Required APIs

Ensure you have the following APIs enabled:

- [Xing API](https://dev.xing.com/)

### Required Scopes for Xing SSO

These are the API scopes required for Xing SSO:

- https://api.xing.com/v1/users/me
- https://api.xing.com/v1/authorize

### Example Usage

Below is an example of how you can use the Xing SSO module in your Python application:

```python
from sso.xing import xing_sso

# Provide the authorization code you received from Xing's authorization server
auth_code = "your_authorization_code"
redirect_uri = "your_redirect_uri"  # This should match the redirect URI specified in your Xing application settings

# Initialize Xing SSO
xing_sso_instance = xing_sso(code=auth_code, redirect_uri=redirect_uri)

# Retrieve user information
user_info = xing_sso_instance.user_info
print(f"User's email: {user_info['email']}")
print(f"User's first name: {user_info['first_name']}")
print(f"User's last name: {user_info['last_name']}")

# Optionally, send an email using the Xing API (replace the placeholders with actual values)
to_address = "recipient@example.com"
subject = "Test Email"
message_text = "Hello, this is a test email from Xing SSO!"
sending_result = xing_sso_instance.send_email(to=to_address, subject=subject, message_text=message_text)
print(f"Email sending result: {sending_result}")
```

### Error Handling

If accessing user information or sending an email fails, the module will raise an `HTTPException` with a status code of 400 and a detailed error message.

### Important Notes

1. Ensure that your application with Xing has the necessary permissions and that you handle token expiration and refresh scenarios.
2. Be sure to handle and store sensitive information (like your client secret) securely.

Following the example for Xing SSO, this documentation should help you quickly and easily set up your environment variables and use the Xing SSO module effectively.