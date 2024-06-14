# Spotify SSO Integration Documentation

This document outlines the steps required to integrate Spotify Single Sign-On (SSO) into your application, including how to set up the necessary environment variables and acquire the necessary API keys.

## Required Environment Variables

To use Spotify SSO, you need to set the following environment variables:

1. `SPOTIFY_CLIENT_ID`: Your Spotify OAuth client ID.
2. `SPOTIFY_CLIENT_SECRET`: Your Spotify OAuth client secret.

Ensure you have set these variables in your `.env` file.

## Steps to Acquire Spotify Client ID and Client Secret

1. **Create a Spotify Developer Account**

   If you don't have a Spotify Developer account, create one by registering at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

2. **Create an App**

   Once you are logged in to the Spotify Developer Dashboard, create a new application:
   - Go to **Dashboard**.
   - Click on the **Create an App** button.
   - Fill out the **App Name** and **App Description** fields.
   - Check the **I understand and accept the Spotify Developer Terms of Service**.
   - Click **Create**.

3. **Retrieve Your Client ID and Client Secret**

   After creating the app, you will be redirected to your app's dashboard:
   - Find the **Client ID** and **Client Secret** on this page.
   - Add these values to your `.env` file as shown below:

     ```
     SPOTIFY_CLIENT_ID=your-client-id
     SPOTIFY_CLIENT_SECRET=your-client-secret
     ```

## Required APIs and Scopes for Spotify SSO

You need to enable the necessary scopes to allow your application to access user data and functionalities:

- `user-read-email`: Allows reading user's email.
- `user-read-private`: Allows reading user's subscription details.
- `playlist-read-private`: Allows reading user's private playlists.

## Code Implementation

The provided code integrates Spotify SSO using the environment variables set earlier. The `SpotifySSO` class handles the SSO process, including getting user information and refreshing access tokens.

### SpotifySSO Class

- **Initialization**: Accepts `access_token` and `refresh_token`. Retrieves the client ID and secret from environment variables and fetches user information.
- **get_new_token**: Refreshes the access token using the refresh token.
- **get_user_info**: Gets user information from the Spotify API. If the access token is expired, it gets a new one and retries.
- **send_email**: Prepares an email message in a format that can be used for sending emails (Note: Spotify does not have a direct API for sending emails).

### spotify_sso Function

- Accepts `code` and `redirect_uri`.
- Exchange the authorization code for access and refresh tokens using the Spotify API.

### Example Usage

```python
from spotify import spotify_sso

# After redirect from Spotify's auth page
code = "AUTHORIZATION_CODE_FROM_SPOTIFY"
redirect_uri = "REDIRECT_URI_REGISTERED_WITH_SPOTIFY"

# Initiate Spotify SSO
spotify_user = spotify_sso(code, redirect_uri)

if spotify_user:
    # Access user info
    print(spotify_user.user_info)
else:
    print("Spotify SSO failed.")
```

Ensure you have the following environment variable set:

```ini
MAGIC_LINK_URL=your-redirect-uri
```

By following these steps and using the provided code, you can set up Spotify SSO in your application quickly and easily.