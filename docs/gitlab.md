# GitLab SSO Integration

This guide walks you through integrating GitLab single sign-on (SSO) with your application. Using GitLab SSO, you can enable users to authenticate using their GitLab accounts.

## Required Environment Variables

To set up GitLab SSO, two key environment variables need to be configured:

- `GITLAB_CLIENT_ID`: This is the OAuth client ID from your GitLab application.
- `GITLAB_CLIENT_SECRET`: This is the OAuth client secret from your GitLab application.

### Steps to Acquire GitLab Client ID and Client Secret:

1. **Create a GitLab OAuth Application:**
   - Go to [GitLab Sign-In](https://gitlab.com/users/sign_in) and log in using your credentials.
   - Go to your GitLab [Profile Settings](https://gitlab.com/profile/applications).
   - Click on `New application`.

2. **Configure the Application:**
   - Enter the `Name` for your application (e.g., "MyAppSSO").
   - Fill in the `Redirect URI` field with the URL to which your application will redirect after successful authentication (e.g., `http://localhost:8000/callback`).
   - Under `Scopes`, select `read_user`, `api`, and `email`.
   - Click on `Save application`.

3. **Retrieve Your Credentials:**
   - After saving, GitLab will provide a `Application ID` (which corresponds to `GITLAB_CLIENT_ID`) and `Secret` (which corresponds to `GITLAB_CLIENT_SECRET`).
   - Set these values in your environment variables or `.env` file:
     ```env
     GITLAB_CLIENT_ID=your_client_id
     GITLAB_CLIENT_SECRET=your_client_secret
     ```

## Required Scopes for GitLab SSO

When creating your OAuth application on GitLab, ensure that you select the following scopes:

- `read_user`: Allows reading the authenticated user’s profile data.
- `api`: Full access to the authenticated user's API.
- `email`: Access to the authenticated user's email address.

These scopes are necessary for retrieving user information such as name and email.

## How to Use the GitLabSSO Class

### Instantiating GitLabSSO

To initiate the OAuth flow, direct users to the GitLab authorization endpoint. After they authorize, GitLab will redirect them to the specified `redirect_uri` with a `code`. Use this `code` to fetch the tokens and initialize the `GitLabSSO` class.

```python
from sso.gitlab import gitlab_sso

code = "authorization_code_received_from_gitlab"
redirect_uri = "your_redirect_uri"  # Optional, defaults to MAGIC_LINK_URL in environment variables

gitlab_sso_instance = gitlab_sso(code, redirect_uri)

# Access user information
user_info = gitlab_sso_instance.user_info
print(user_info)
```

### Example

```python
from sso.gitlab import GitLabSSO

# After redirect, extract 'code' param from the query string
code = "your_authorization_code"

# Initialize SSO instance
gitlab_instance = GitLabSSO(code)

# Retrieve user information
user_info = gitlab_instance.user_info
print(user_info)  # {'email': 'user@example.com', 'first_name': 'First', 'last_name': 'Last'}
```

### Handling Token Refresh

If the access token expires, the `GitLabSSO` class will automatically handle refreshing it using the `refresh_token`:

```python
g_instance = GitLabSSO(access_token=current_access_token, refresh_token=current_refresh_token)

# Attempt to retrieve user information, will refresh token if needed
user_info = g_instance.user_info
print(user_info)
```

### Error Handling

If there is an issue with retrieving the user information, an `HTTPException` is raised:

```python
try:
    user_info = gitlab_instance.user_info
except HTTPException as e:
    print("Error fetching user information:", e.detail)
```

## Note

GitLab's API does not provide a direct method to send emails. The `send_email` method in the `GitLabSSO` class raises a `NotImplementedError`. You would need to use a separate email service like SendGrid or SMTP to handle emails.

```python
def send_email(self, to, subject, message_text):
    raise NotImplementedError("GitLab SSO does not support sending emails directly.")
```

Ensure you follow the GitLab [OAuth documentation](https://docs.gitlab.com/ee/api/oauth2.html) for the most up-to-date and detailed information on scopes, endpoints, and OAuth flow.