## Reddit SSO Integration

This module allows you to integrate Reddit Single Sign-On (SSO) into your application. By using this module, you can authenticate via Reddit, retrieve user information, and even submit posts to a subreddit on behalf of a user. The code leverages the Reddit OAuth2.0 for authentication and authorization.

### Required Environment Variables

Before you begin, you'll need to set up the following environment variables in your `.env` file:

- `REDDIT_CLIENT_ID`: Your Reddit application's client ID.
- `REDDIT_CLIENT_SECRET`: Your Reddit application's client secret.

### Required APIs

Make sure you have a Reddit OAuth application set up. You can create one by following these steps:

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps).
2. Scroll down to "Developed Applications" and click on `Create App`.
3. Fill in the application name, and choose `script` as the type.
4. Set the `redirect_uri` to a valid URL where you will receive the authorization code (e.g., `http://localhost:8000/reddit_callback`).
5. Note down the `client ID` and `client secret` from the created application.
6. Add the `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` to your `.env` file.

### Required Scopes for Reddit OAuth

Ensure that your Reddit OAuth application requests the following scopes:

- `identity`: Access to the user’s Reddit identity.
- `submit`: Ability to submit and edit content.
- `read`: Ability to read private messages and save content.

### Setting Up Your Environment

1. **Install Required Packages:** Ensure you have `requests` and `fastapi` installed in your Python environment.

   ```sh
   pip install requests fastapi
   ```

2. **Create a `.env` File:** Add the necessary environment variables:

   ```
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   ```

3. **Implement the Module:** Use the `reddit.py` module to interact with the Reddit API.

### Usage

#### reddit_sso Function

This function initializes the Reddit SSO process and returns an instance of `RedditSSO` class with access and refresh tokens.

##### Parameters

- `code`: The authorization code received from Reddit after user authentication.
- `redirect_uri` (optional): The URL to which Reddit will redirect after authentication.

##### Returns

- An instance of the `RedditSSO` class initialized with access and refresh tokens.

##### Example

```python
from sso.reddit import reddit_sso

redirect_uri = "http://localhost:8000/reddit_callback"
auth_code = "your_authorization_code"
reddit_instance = reddit_sso(code=auth_code, redirect_uri=redirect_uri)

if reddit_instance:
    print(reddit_instance.user_info)
else:
    print("Failed to authenticate with Reddit")
```

### RedditSSO Class

The `RedditSSO` class provides methods to interact with the Reddit API.

#### Methods

- `__init__`: Initializes the class with access and refresh tokens and retrieves user information.
- `get_new_token`: Refreshes the access token using the refresh token.
- `get_user_info`: Retrieves the authenticated user's information.
- `submit_post`: Submits a post to a specified subreddit.

### Example Usage

#### Initializing and Fetching User Info

```python
reddit_instance = RedditSSO(access_token="your_access_token", refresh_token="your_refresh_token")
print(reddit_instance.user_info)
```

#### Submitting a Post

```python
subreddit = "test"
title = "My First Post"
content = "Hello, Reddit!"
response = reddit_instance.submit_post(subreddit, title, content)
print(response)
```

### Error Handling

The module uses `logging` to report errors encountered while fetching access tokens or submitting posts. It also raises an `HTTPException` with a 400 status code if it fails to retrieve user information.

By following the above steps, you can seamlessly integrate Reddit SSO into your Python application. Feel free to modify the code as per your specific requirements.