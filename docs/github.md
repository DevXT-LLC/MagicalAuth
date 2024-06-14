# GitHub Single Sign-On Implementation

This documentation details how to implement GitHub Single Sign-On (SSO) in your application using the provided `GitHubSSO` class and related functions.

## Required Environment Variables

To use the `GitHubSSO` class, you need to have the following environment variables set:

- `GITHUB_CLIENT_ID`: GitHub OAuth client ID
- `GITHUB_CLIENT_SECRET`: GitHub OAuth client secret

## Required Scopes for GitHub OAuth

Ensure your GitHub OAuth application requests the following scopes to access the necessary user information:

- `user:email`
- `read:user`

## How to Acquire GitHub OAuth Client ID and Client Secret

1. **Register a new OAuth application on GitHub:**
   - Go to GitHub's developer settings: [GitHub Developer Settings](https://github.com/settings/developers)
   - Click on `New OAuth App`.
   - Fill in the required fields:
     - **Application name**: Your application’s name.
     - **Homepage URL**: The URL to your application's homepage.
     - **Authorization callback URL**: The redirect URI where users will be sent after authorization. This should match the `redirect_uri` parameter in your authorization request.
   - Click `Register application`.

2. **Get the client credentials:**
   - After registering, you will see your new application listed on the OAuth Apps page.
   - Click on the application to see its details.
   - Copy the `Client ID` and `Client Secret` to use as environment variables in your application.

3. **Set Environment Variables:**
   - Add the `Client ID` and `Client Secret` to your environment variables. This can be done in your `.env` file like so:
     ```
     GITHUB_CLIENT_ID=your_client_id
     GITHUB_CLIENT_SECRET=your_client_secret
     ```
   - Replace `your_client_id` and `your_client_secret` with the actual values you copied from GitHub.

# Implementation Details

## GitHub SSO Workflow

The GitHub SSO process involves two main steps:
1. **Getting the Access Token:**
    ```python
    def github_sso(code, redirect_uri=None) -> GitHubSSO:
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
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": getenv("GITHUB_CLIENT_ID"),
                "client_secret": getenv("GITHUB_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        if response.status_code != 200:
            logging.error(f"Error getting GitHub access token: {response.text}")
            return None, None
        data = response.json()
        access_token = data["access_token"]
        refresh_token = data.get("refresh_token", "Not provided")
        return GitHubSSO(access_token=access_token, refresh_token=refresh_token)
    ```

    Here, the `github_sso` function exchanges an authorization code for an access token from GitHub. The `access_token` is then used to make authenticated requests to fetch user information.

2. **Fetching User Information:**
    ```python
    class GitHubSSO:
        def __init__(self, access_token=None, refresh_token=None):
            self.access_token = access_token
            self.refresh_token = refresh_token
            self.client_id = getenv("GITHUB_CLIENT_ID")
            self.client_secret = getenv("GITHUB_CLIENT_SECRET")
            self.user_info = self.get_user_info()

        def get_user_info(self):
            uri = "https://api.github.com/user"
            response = requests.get(
                uri,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            if response.status_code == 401:
                self.access_token = self.get_new_token()
                response = requests.get(
                    uri,
                    headers={"Authorization": f"Bearer {self.access_token}"},
                )
            try:
                data = response.json()
                email_response = requests.get(
                    "https://api.github.com/user/emails",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                )
                email_data = email_response.json()
                primary_email = next(
                    email["email"] for email in email_data if email["primary"]
                )
                return {
                    "email": primary_email,
                    "first_name": (
                        data.get("name", "").split()[0] if data.get("name") else ""
                    ),
                    "last_name": (
                        data.get("name", "").split()[-1] if data.get("name") else ""
                    ),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail="Error getting user info from GitHub",
                )
    ```

    The `GitHubSSO` class fetches user details from the GitHub API using the access token. If the access token is expired or invalid, it attempts to refresh the token.

Note: GitHub does not provide refresh tokens directly. You would need to re-authorize the user to get a new access token.

Use this class and function in your application to handle GitHub SSO and retrieve user information seamlessly.