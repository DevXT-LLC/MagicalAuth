# Instagram SSO Documentation

## Overview

This module provides Single Sign-On (SSO) capabilities for Instagram using OAuth. The integration allows you to authenticate users, fetch user profile information, and publish media posts on behalf of users.

## Required Environment Variables

To start using Instagram SSO, you need to provide the following environment variables:

- `INSTAGRAM_CLIENT_ID`: Instagram OAuth client ID
- `INSTAGRAM_CLIENT_SECRET`: Instagram OAuth client secret
- `MAGIC_LINK_URL`: The redirect URL for the OAuth process

Add these environment variables to your `.env` file.

## Required APIs

Ensure that the Instagram Basic Display API is enabled for your application. This is necessary to authenticate users and fetch user profile information.

## Required Scopes for Instagram OAuth

When setting up your Instagram OAuth client, make sure to include the following scopes to request necessary permissions:

- `user_profile`
- `user_media`

## Setup Steps

Follow these steps to acquire your keys and set up the required environment variables:

### 1. Create or Sign into an Instagram Developer Account

- Go to the [Instagram Developer Documentation](https://developers.facebook.com/docs/instagram-basic-display-api/getting-started).
- Sign in using your Facebook account associated with your Instagram Business Account.

### 2. Create a New Instagram App

- Navigate to the "My Apps" section and click "Create App."
- Choose the "For Everything Else" option and click "Next."
- Provide an app name and your contact email, then click "Create App ID."

### 3. Add Instagram Basic Display

- In your newly created app dashboard, locate and click "Add Product" in the sidebar.
- Find "Instagram" in the list and click "Set Up."
- In the Instagram Basic Display section, click "Create New App".

### 4. Configure Instagram OAuth

- Once the app is created, visit the "Basic Display" settings under the "Instagram" product.
- Define the redirect URI (`MAGIC_LINK_URL`) for your app.
- Add the necessary OAuth redirect URI based on your application's configuration.

### 5. Retrieve the Client ID and Client Secret

- In the "Basic Display" section, you should see your `Client ID` and `Client Secret`.
- Copy these values and add them to your `.env` file as `INSTAGRAM_CLIENT_ID` and `INSTAGRAM_CLIENT_SECRET`.

### 6. Finalize Setup

- Ensure that you've configured the required scopes (`user_profile`, `user_media`) under the Instagram Basic Display settings.
- Save all changes and ensure that the app status is live.

### 7. Environment Variable Configuration

Ensure your `.env` file looks something like:

```plaintext
INSTAGRAM_CLIENT_ID=your_client_id_here
INSTAGRAM_CLIENT_SECRET=your_client_secret_here
MAGIC_LINK_URL=https://your-redirect-url.com
```

## Example

### Usage

Here's an example of how to use the `InstagramSSO` class in your application:

```python
from sso.instagram import InstagramSSO, instagram_sso

# After the user approved access in Instagram, you will receive a `code`
authorization_code = 'received_auth_code'
redirect_uri = 'https://your-redirect-url.com'

# Acquiring Instagram SSO
instagram_sso_instance = instagram_sso(authorization_code, redirect_uri)

# Fetching user info
user_info = instagram_sso_instance.user_info
print(user_info)

# Sending a media post
image_url = 'https://example.com/image.jpg'
caption = "Your caption text"
response = instagram_sso_instance.send_media_post(image_url, caption)
print(response)
```

This example demonstrates initializing an Instagram SSO instance after receiving an authorization code, fetching user information, and posting media on behalf of the user.

By following this documentation, users can quickly and efficiently set up their environment variables and start utilizing Instagram SSO within their applications.