# Stack Exchange SSO Guide

This guide provides detailed instructions on how to set up and use Stack Exchange Single Sign-On (SSO) in your application. Please follow each step carefully to ensure successful integration.

## Required Environment Variables

To utilize Stack Exchange SSO, you need to set the following environment variables in your `.env` file:

- `STACKEXCHANGE_CLIENT_ID`: Your Stack Exchange OAuth client ID.
- `STACKEXCHANGE_CLIENT_SECRET`: Your Stack Exchange OAuth client secret.
- `STACKEXCHANGE_KEY`: (Optional) A key for additional API requests (can enhance rate limits).

## Setting Up Stack Exchange OAuth Credentials

1. **Create a Stack Exchange Application:**
   - Go to the [Stack Exchange API Applications](https://stackapps.com/apps/oauth/register) page.
   - Click the "Register Your Application" button.
   - Fill in the required details such as Application Name, Description, Organization Information, etc.
   - Set the OAuth Redirect URL (you will need this URL for redirect_uri).
   - After their review, you will obtain the `Client ID` and `Client Secret` which are needed for the environment variables.

2. **Enable Required Scopes:**
   - The application will need the following scopes to function properly:
     - read_inbox
     - no_expiry
     - private_info
     - write_access

3. **Add the Environment Variables:**
   - Create a `.env` file at the root of your project if it does not exist already.
   - Add the following lines to the file with your corresponding credentials:
     ```env
     STACKEXCHANGE_CLIENT_ID=your_stack_exchange_client_id
     STACKEXCHANGE_CLIENT_SECRET=your_stack_exchange_client_secret
     STACKEXCHANGE_KEY=your_stack_exchange_key
     ```

## Integrate Stack Exchange SSO in Your Code

Here's an outline of the main components necessary for integrating Stack Exchange SSO:

### stack_exchange_sso Function
This function handles the retrieval of an access token using an authorization code.

```python
def stack_exchange_sso(code, redirect_uri=None) -> StackExchangeSSO:
    if not redirect_uri:
        redirect_uri = getenv("MAGIC_LINK_URL")
    code = (
        str(code)
        .replace("%2F", "/")
        .replace("%3D", "=")
        .replace("%3F", "?")
        .replace("%3D", "=")
    )
    response = requests.post(
        f"https://stackexchange.com/oauth/access_token",
        data={
            "client_id": getenv("STACKEXCHANGE_CLIENT_ID"),
            "client_secret": getenv("STACKEXCHANGE_CLIENT_SECRET"),
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    if response.status_code != 200:
        logging.error(f"Error getting Stack Exchange access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"] if "refresh_token" in data else "Not provided"
    return StackExchangeSSO(access_token=access_token, refresh_token=refresh_token)
```

### StackExchangeSSO Class
This class manages the SSO operations, including fetching user info and refreshing tokens.

```python
class StackExchangeSSO:
    def __init__(
        self,
        access_token=None,
        refresh_token=None,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = getenv("STACKEXCHANGE_CLIENT_ID")
        self.client_secret = getenv("STACKEXCHANGE_CLIENT_SECRET")
        self.key = getenv("STACKEXCHANGE_KEY")
        self.user_info = self.get_user_info()

    def get_new_token(self):
        response = requests.post(
            "https://stackexchange.com/oauth/access_token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
                "scope": "read_inbox no_expiry private_info write_access",
            },
        )
        return response.json()["access_token"]

    def get_user_info(self):
        response = requests.get(
            f"https://api.stackexchange.com/2.2/me",
            params={
                "access_token": self.access_token,
                "key": self.key,
                "site": "stackoverflow",
            },
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.get(
                f"https://api.stackexchange.com/2.2/me",
                params={
                    "access_token": self.access_token,
                    "key": self.key,
                    "site": "stackoverflow",
                },
            )
        try:
            data = response.json()["items"][0]
            display_name = data["display_name"]
            email = data[
                "email"
            ]  # Note: Stack Exchange does not provide email directly
            return {
                "display_name": display_name,
                "email": email,
            }
        except:
            raise HTTPException(
                status_code=400,
                detail="Error getting user info from Stack Exchange",
            )
```

Remember to handle the authorization flow in your frontend, ensuring that you get the authorization code which is then passed to the backend to obtain the tokens using the `stack_exchange_sso` function.

By following these instructions, you will successfully set up Stack Exchange SSO in your application, allowing users to authenticate using their Stack Exchange accounts, and granting the necessary permissions for your application to function correctly.