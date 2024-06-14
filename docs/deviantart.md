## DeviantArt SSO Integration Guide

This guide will help you set up and integrate deviantART Single Sign-On (SSO) using OAuth2 in your application. Please follow the steps carefully to ensure seamless integration.

### Required Environment Variables

To start using deviantART SSO, you need to set up the following environment variables in your environment. You can add these variables to your `.env` file:

- `DEVIANTART_CLIENT_ID`: deviantART OAuth client ID
- `DEVIANTART_CLIENT_SECRET`: deviantART OAuth client secret

### How to Acquire deviantART Client ID and Client Secret

1. **Register your Application**:
   - Log in to your deviantART account.
   - Navigate to the [deviantART OAuth2 Application Registration page](https://www.deviantart.com/settings/applications).
   - Click on "Register a new application" to create a new application.
   - Fill out the necessary details such as application name, description, and set the redirect URI (e.g., `http://localhost:8000/callback` for local testing).
   
2. **Retrieve Client ID and Client Secret**:
   - After successfully registering your application, you will be provided with a `Client ID` and `Client Secret`.
   - Store these credentials in a safe place.
   - Add them to your `.env` file as follows:
     ```
     DEVIANTART_CLIENT_ID=your_client_id
     DEVIANTART_CLIENT_SECRET=your_client_secret
     ```

### Required OAuth Scopes for deviantART

The following OAuth scopes are required for deviantART SSO to work properly:

- `user`
- `browse`
- `stash`
- `send_message`

These scopes allow the application to access user information, browse deviantART content, access stash, and send messages on behalf of the user.

### Implementing deviantART SSO in Your Application

The provided Python script (`./sso/deviantart.py`) facilitates the integration of deviantART SSO in your application. Below is a step-by-step guide on how to use this script:

1. **Initialization**:
   Create a new instance of the `DeviantArtSSO` class by providing the necessary credentials.

   ```python
   from sso.deviantart import deviantart_sso

   # Use the authorization code received from deviantART to acquire tokens
   code = "auth_code_received_from_deviantart"
   redirect_uri = "http://localhost:8000/callback"  # or your registered redirect URI
   deviantart_instance = deviantart_sso(code, redirect_uri)
   ```

2. **Get User Information**:
   Once the instance is created, you can fetch the user information using the `get_user_info` method.

   ```python
   user_info = deviantart_instance.user_info
   print(user_info)  # Output: {'email': '...', 'first_name': '...', 'last_name': '...'}
   ```

3. **Send Messages**:
   To send messages on behalf of the user, use the `send_message` method.

   ```python
   to = "recipient_username"
   subject = "This is a test message"
   message_text = "Hello, this is a message sent from my app using deviantART SSO."

   response = deviantart_instance.send_message(to, subject, message_text)
   print(response)  # Output: JSON response from deviantART API
   ```

### Handling Token Expiry

The script includes handling for token expiry. If the access token has expired (HTTP 401 response), the script automatically fetches a new token using the refresh token and retries the request.

### Error Handling

The script uses HTTPException to handle errors gracefully. If there's any error while fetching user information or sending messages, the script will raise an appropriate HTTPException with a status code and detail message.

By following this guide and using the provided script, you can seamlessly integrate deviantART SSO into your application. If you encounter any issues or need further assistance, please refer to the deviantART API documentation or the support forums.