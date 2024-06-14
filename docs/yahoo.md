## Yahoo SSO

The `YahooSSO` class and the `yahoo_sso` function facilitate Single Sign-On (SSO) with Yahoo, allowing you to retrieve user information (email, first name, last name) and send emails through Yahoo's mail services. Yahoo SSO requires specific OAuth credentials and certain API permissions to function properly.

### Required Environment Variables

To configure Yahoo SSO, you need to set the following environment variables. Add them to your `.env` file:

- `YAHOO_CLIENT_ID`: Yahoo OAuth client ID
- `YAHOO_CLIENT_SECRET`: Yahoo OAuth client secret

### Acquiring Yahoo OAuth Credentials

1. **Create a Yahoo Developer Account:**
   - Go to the [Yahoo Developer Network](https://developer.yahoo.com).
   - Sign in with your Yahoo account or create a new one.

2. **Create an App and Obtain Client ID and Secret:**
   - Navigate to the [Yahoo Developer Dashboard](https://developer.yahoo.com/apps/).
   - Click on "Create an App".
   - Fill in the required details such as application name, description, and Redirect URI.
   - Select the required permissions: `profile`, `email`, and `mail-w`.
   - After creating the app, you will be provided with the `Client ID` and `Client Secret`. Note these down as you'll need to add them to your environment variables.
  
3. **Add Redirect URI:**
   - Ensure that you have specified a valid Redirect URI in your app settings. This URI is where Yahoo will redirect users after authentication with the authorization code.
   - Example Redirect URI: `https://yourdomain.com/oauth/callback/yahoo`.
   - Add this URI to the `MAGIC_LINK_URL` environment variable if required.

### Required APIs and Scopes

Ensure that your Yahoo app has the following scopes enabled:

- `profile`
- `email`
- `mail-w`

These scopes allow your application to view user profiles, retrieve email addresses, and send emails.

### Setting Up Your Environment Variables

Add the following lines to your `.env` file:

```plaintext
YAHOO_CLIENT_ID=your_yahoo_client_id
YAHOO_CLIENT_SECRET=your_yahoo_client_secret
MAGIC_LINK_URL=https://yourdomain.com/oauth/callback/yahoo
```

Replace `your_yahoo_client_id` and `your_yahoo_client_secret` with the credentials you obtained from the Yahoo Developer Dashboard. Set `MAGIC_LINK_URL` to your application's redirect URI.

### Example Usage

Here is a simple example of how to initialize the `YahooSSO` class and retrieve user information or send an email. 

```python
from sso.yahoo import yahoo_sso

# Example function to handle OAuth code and retrieve user information
def handle_oauth(code, redirect_uri):
    yahoo_sso_instance = yahoo_sso(code, redirect_uri)
    if yahoo_sso_instance:
        user_info = yahoo_sso_instance.user_info
        print(f"User Email: {user_info['email']}")
        print(f"First Name: {user_info['first_name']}")
        print(f"Last Name: {user_info['last_name']}")
    else:
        print("Failed to authenticate with Yahoo.")

# Example function to send email using Yahoo SSO
def send_yahoo_mail(access_token, refresh_token, to, subject, message_text):
    yahoo_sso_instance = YahooSSO(access_token=access_token, refresh_token=refresh_token)
    response = yahoo_sso_instance.send_email(to, subject, message_text)
    print(f"Email send response: {response}")

# Replace with actual values for OAuth code and tokens
oauth_code = "sample_oauth_code"
redirect_uri = "https://yourdomain.com/oauth/callback/yahoo"
access_token = "sample_access_token"
refresh_token = "sample_refresh_token"

# Retrieve user information
handle_oauth(oauth_code, redirect_uri)

# Send email
send_yahoo_mail(access_token, refresh_token, "recipient@example.com", "Hello!", "This is an email sent using Yahoo SSO.")
```

Ensure you have configured the environment variables and obtained the required OAuth credentials before running the example. This will enable your application to interact with Yahoo's APIs and perform the necessary actions using Yahoo SSO.