## Ping Identity SSO

This section explains how to set up Single Sign-On (SSO) with Ping Identity using the provided `ping_identity.py` script. The script handles OAuth authentication and allows users to fetch user information and send emails via Ping Identity. Follow the steps below to configure and use the Ping Identity SSO integration.

### Required Environment Variables

- `PING_IDENTITY_CLIENT_ID`: Ping Identity OAuth client ID
- `PING_IDENTITY_CLIENT_SECRET`: Ping Identity OAuth client secret

### Required APIs

Ensure that you have the following APIs enabled for your Ping Identity application. You can enable these APIs through the Ping Identity admin dashboard.

1. **UserInfo API**: Used to fetch user information.
2. **Email API**: Used to send emails on behalf of the user.

### Acquiring Required Keys

#### Steps to Acquire `PING_IDENTITY_CLIENT_ID` and `PING_IDENTITY_CLIENT_SECRET`

1. **Log in to Ping Identity Admin Portal**: Access the Ping Identity admin portal.

2. **Create an OAuth Client**: 
   - Go to the 'Connections' tab.
   - Select 'Applications' and click 'Add Application' to create a new OAuth client.
   - Fill in the required details (application name, description, etc.) and select the OAuth grant type you intend to use (Authorization Code Grant in most cases).

3. **Configure Callback URL**:
   - Set the Redirect URI in your application settings to the endpoint where Ping Identity will send authorization responses (e.g., `https://your-app.com/callback`).

4. **Obtain Client ID and Client Secret**:
   - After creating the OAuth client, you will be provided with a `Client ID` and `Client Secret`. Save these credentials securely, as they will be required in your application.

5. **Enable Necessary Scopes**:
   - Ensure your OAuth client is configured to request the necessary scopes:
     - `profile`
     - `email`
     - `openid`

### Setup Environment Variables

1. **Define Environment Variables**:
   - Add the following lines to your `.env` file, replacing the placeholders with your actual client ID and client secret.

    ```
    PING_IDENTITY_CLIENT_ID=your_client_id
    PING_IDENTITY_CLIENT_SECRET=your_client_secret
    MAGIC_LINK_URL=your_magic_link_url
    ```

### Using the Provided Script

#### Initialize Ping Identity SSO

Create an instance of `PingIdentitySSO` using the authorization code received from the OAuth flow.

```python
from sso.ping_identity import ping_identity_sso

code = 'your_authorization_code'
redirect_uri = 'https://your-app.com/callback'
ping_sso = ping_identity_sso(code, redirect_uri)

if ping_sso:
    user_info = ping_sso.user_info
    print("User Info:", user_info)
else:
    print("Failed to initialize PingIdentitySSO.")
```

#### Send Emails

Use the `send_email` method to send emails on behalf of the authenticated user.

```python
to_email = "recipient@example.com"
subject = "Test Email"
message_text = "This is a test email."
response = ping_sso.send_email(to_email, subject, message_text)
print("Email Sending Response:", response)
```

### Handling Token Refresh

The script is designed to handle token refresh automatically. If an access token expires, the script will attempt to use the refresh token to get a new access token.

#### Example of Fetching User Info

```python
ping_sso = ping_identity_sso(code, redirect_uri)
if ping_sso:
    user_info = ping_sso.user_info
    print("User Info:", user_info)
else:
    print("Failed to fetch user info.")
```

By following these steps, you should be able to quickly set up and use Ping Identity SSO within your application. For more information on Ping Identity and OAuth setup, refer to the [Ping Identity Documentation](https://www.pingidentity.com/en/resources/oauth2-developers-guide.html).