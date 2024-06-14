# LinkedIn SSO Integration

## Overview

This document provides a guide for setting up LinkedIn Single Sign-On (SSO) integration in your application. Follow the steps below to configure the LinkedIn OAuth client and obtain the necessary keys and permissions.

## Required Environment Variables

To integrate LinkedIn SSO, you need to set the following environment variables in your `.env` file:

- `LINKEDIN_CLIENT_ID`: LinkedIn OAuth client ID
- `LINKEDIN_CLIENT_SECRET`: LinkedIn OAuth client secret

## Steps to Acquire LinkedIn OAuth Credentials

Follow these steps to obtain the required LinkedIn OAuth credentials:

1. **Create a LinkedIn Application**
    - Navigate to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
    - Log in with your LinkedIn account.
    - Click on "Create App" and fill in the required details.
    - After the app is created, you will be redirected to the app's dashboard.

2. **Obtain Client ID and Client Secret**
    - In the app's dashboard, locate `Client ID` and `Client Secret` under the "Auth" tab.
    - Copy these values and add them to your `.env` file as `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET`.

3. **Set Up Redirect URI**
    - Ensure you set up the correct Redirect URI. This URI should match the one used in your application. You can set this URI in the app's "Auth" tab.

## Required APIs and Scopes

To enable LinkedIn SSO, you must ensure that your application has access to the following APIs and scopes:

### Required APIs

- No additional APIs are needed other than LinkedIn's default OAuth APIs.

### Required Scopes for LinkedIn OAuth

- `r_liteprofile`: Grants access to retrieve the user's profile.
- `r_emailaddress`: Grants access to retrieve the user's email address.
- `w_member_social`: Grants access to post and share content on LinkedIn.

Ensure that these scopes are requested during the OAuth authorization process.

## Setting Environment Variables

Add the obtained credentials and required environment variables to your `.env` file:

```env
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
```

Additionally, ensure you have `MAGIC_LINK_URL` in your `.env` file if it's being used as the redirect URI:

```env
MAGIC_LINK_URL=your_redirect_uri
```

## Example Usage

Here is an example of how you can use the LinkedInSSO class and the `linkedin_sso` function in your application:

```python
from linkedin import linkedin_sso

# Assume `code` is received from LinkedIn after user authorization
code = "authorization_code_received_from_linkedin"
redirect_uri = "your_redirect_uri"  # optional, defaults to MAGIC_LINK_URL

linkedin_sso_instance = linkedin_sso(code, redirect_uri)

if linkedin_sso_instance:
    user_info = linkedin_sso_instance.user_info
    print("User Info:", user_info)
else:
    print("Failed to authenticate with LinkedIn.")
```

### Notes

- **Token Management**: The `LinkedInSSO` class handles token refreshing if the access token expires.
- **Error Handling**: The class raises an `HTTPException` if it fails to retrieve user information from LinkedIn.

## Conclusion

By following these steps, you can integrate LinkedIn SSO into your application seamlessly. Ensure all necessary permissions and APIs are enabled, and properly manage environment variables.