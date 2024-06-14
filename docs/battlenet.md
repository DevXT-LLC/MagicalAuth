## Battle.net SSO Integration

This guide will help you set up Battle.net single sign-on (SSO) integration using OAuth2. Follow the instructions to acquire the necessary keys and configure your environment variables.

### Required Environment Variables

Before you begin, make sure to add the following environment variables to your `.env` file:

- `BATTLENET_CLIENT_ID`: Battle.net OAuth client ID
- `BATTLENET_CLIENT_SECRET`: Battle.net OAuth client secret

### Obtaining Battle.net Client ID and Client Secret

To get your Battle.net Client ID and Client Secret, follow these steps:

1. **Create a Battle.net Developer Account:**
   - Go to the [Battle.net Developer Portal](https://develop.battle.net/access/).
   - Sign in using your Battle.net account credentials.

2. **Create an Application:**
   - Navigate to the "Create Client" section and fill out the required details about your application.
   - After creating the application, you will be provided with a `Client ID` and `Client Secret`.

3. **Enable APIs:**
   - Ensure that the necessary APIs are enabled for your Battle.net application. This generally includes the OAuth2 authentication API.

4. **Add Redirect URI:**
   - Configure the redirect URI to match the URL where you want to receive the authorization code.

### Required Scopes for Battle.net OAuth

Ensure you request the following scopes when setting up your SSO integration:

- `openid`
- `email`

These scopes will grant your application access to basic Battle.net profile information and the user's email address.

### Environment Variables Configuration

After you have your `Client ID` and `Client Secret`, add them to your `.env` file like so:

```plaintext
# .env
BATTLENET_CLIENT_ID=your_battlenet_client_id
BATTLENET_CLIENT_SECRET=your_battlenet_client_secret
MAGIC_LINK_URL=your_redirect_uri
```

### How It Works

The `BattleNetSSO` class handles the OAuth flow, manages tokens, and retrieves user information from Battle.net.

1. **Initialization:**
   Initialize the `BattleNetSSO` object with optional access and refresh tokens.
   
2. **Obtaining a New Token:**
   Use the `get_new_token` method to refresh your access token using the refresh token.

3. **Retrieving User Information:**
   The `get_user_info` method fetches and returns the user's Battle.net information, including their email and BattleTag.

### battle.net_auth Function

The `battlenet_sso` function initiates the OAuth flow using the authorization code received after user consent. It exchanges the authorization code for an access token and an optional refresh token, then initializes and returns a `BattleNetSSO` instance.

```python
def battlenet_sso(code, redirect_uri=None) -> BattleNetSSO:
    # Function implementation
```

### Example Usage

Here's an example of how to use the `BattleNetSSO` class:

```python
from sso.battlenet import battlenet_sso

# Replace with the actual code received from the authorization response
authorization_code = "received_authorization_code"

# Initialize SSO using the authorization code and optional redirect URI
sso_instance = battlenet_sso(authorization_code, redirect_uri="your_redirect_uri")

if sso_instance:
    user_info = sso_instance.user_info
    print(f"User Email: {user_info['email']}")
    print(f"BattleTag: {user_info['battletag']}")
else:
    print("Failed to initialize Battle.net SSO")
```

### Additional Information

Ensure that your client correctly handles errors and responses, including re-attempting token refreshes and handling HTTP exceptions gracefully.

By following these instructions, you should be able to quickly and easily integrate Battle.net SSO into your application. Happy coding!