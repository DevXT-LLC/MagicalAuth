## Pixiv SSO

This documentation will guide you through setting up Pixiv Single Sign-On (SSO) in your application using the provided `pixiv.py` script. The integration leverages Pixiv's OAuth for user authentication.

### Required Environment Variables

To use Pixiv SSO, you need to set up the following environment variables in your `.env` file:

- `PIXIV_CLIENT_ID`: Your Pixiv OAuth client ID.
- `PIXIV_CLIENT_SECRET`: Your Pixiv OAuth client secret.

### Required APIs

Before setting up your environment variables, ensure you have the necessary Pixiv APIs enabled. Your application will need the following scopes to perform authentication through Pixiv OAuth:

- `pixiv.scope.profile.read`

### How To Acquire Keys

Follow these steps to get your `PIXIV_CLIENT_ID` and `PIXIV_CLIENT_SECRET`:

1. **Create a Pixiv OAuth Application**:
   - Go to the Pixiv developer site and log in with your Pixiv account.
   - Navigate to the section where you can manage your OAuth applications.
   - Create a new application. You will be asked to provide details such as the name and description of your application. Ensure you also specify the required scopes (`pixiv.scope.profile.read`).

2. **Get Client ID and Client Secret**:
   - Once the application is created, Pixiv will provide you with a `client_id` and `client_secret`. These will be your `PIXIV_CLIENT_ID` and `PIXIV_CLIENT_SECRET`.

3. **Add Environment Variables**:
   - Open or create a `.env` file in the root of your project directory.
   - Add the following lines to your `.env` file:
     ```
     PIXIV_CLIENT_ID=your_pixiv_client_id_here
     PIXIV_CLIENT_SECRET=your_pixiv_client_secret_here
     ```

### Setting Up and Using Pixiv SSO

Here's a brief description of the primary classes and functions:

#### PixivSSO Class

This class handles user authentication and token management with Pixiv.

- **Attributes**:
  - `access_token`: Access token for Pixiv API.
  - `refresh_token`: Refresh token for Pixiv API.
  - `client_id`: Pixiv client ID.
  - `client_secret`: Pixiv client secret.
  - `user_info`: Dictionary containing user information like email and first name.

- **Methods**:
  - `get_new_token`: Refreshes the access token using the refresh token.
  - `get_user_info`: Fetches the user's information from Pixiv using the access token.
  - `send_email`: Not implemented, as Pixiv does not support sending emails.

#### pixiv_sso Function

This function initiates the Pixiv OAuth process and returns an instance of `PixivSSO`.

- **Parameters**:
  - `code`: The authorization code received from the Pixiv login flow.
  - `redirect_uri`: Optional URI to redirect to after authentication. Defaults to the `MAGIC_LINK_URL` environment variable.

- **Returns**:
  - An instance of `PixivSSO` initialized with the access and refresh tokens.

### Example Usage

Here is a sample usage of the `pixiv_sso` function:

```python
from dotenv import load_dotenv
import os
load_dotenv()

from sso.pixiv import pixiv_sso

code = "authorization_code_received_from_pixiv"
redirect_uri = "https://your-redirect-uri.com/callback"

pixiv_auth = pixiv_sso(code, redirect_uri)

if pixiv_auth:
    user_info = pixiv_auth.user_info
    print(f"User's email: {user_info['email']}")
    print(f"User's first name: {user_info['first_name']}")
else:
    print("Authentication failed")
```

Ensure that you replace `"authorization_code_received_from_pixiv"` and `"https://your-redirect-uri.com/callback"` with your actual authorization code and redirect URI.

By following these steps, you can successfully integrate Pixiv SSO into your application, facilitating secure user authentication.

For any issues or further details, refer to the [Pixiv Developer Documentation](https://www.pixiv.net/developers/docs).