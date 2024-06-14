## AOL SSO Integration Documentation

This documentation guides you through setting up Single Sign-On (SSO) integration with AOL using OAuth. The OAuth tokens allow you to fetch user information and send emails on behalf of the user. Please note that the endpoints and scopes used in this example are hypothetical and may not reflect the actual endpoints provided by AOL.

### Required Environment Variables

To use AOL SSO, you need to provide specific environment variables. These are necessary for the OAuth client to function correctly.

- `AOL_CLIENT_ID`: Your AOL OAuth client ID.
- `AOL_CLIENT_SECRET`: Your AOL OAuth client secret.

Ensure these variables are set in your environment.

### Steps to Set Up AOL SSO Integration

1. **Acquire OAuth Client ID and Secret**

    - Visit the AOL Developer website (hypothetical https://developer.aol.com/).
    - Navigate to the OAuth section and create a new OAuth application.
    - Note down the `AOL_CLIENT_ID` and `AOL_CLIENT_SECRET` provided by AOL.
    - Make sure to enable the following scopes for your application:
        - `https://api.aol.com/userinfo.profile`
        - `https://api.aol.com/userinfo.email`
        - `https://api.aol.com/mail.send`

2. **Set the Environment Variables**

    Add the acquired client ID and secret to your environment. This could be done by adding them to a `.env` file in the root of your project:

    ```plaintext
    AOL_CLIENT_ID=your_aol_client_id_here
    AOL_CLIENT_SECRET=your_aol_client_secret_here
    ```

3. **Implementing the AOL SSO Class**

    The `AOLSSO` class in the provided code configures the OAuth flow, retrieves user information, and sends emails on behalf of the authenticated user.

    - **Initialization**:
      ```python
      aol_sso_instance = AOLSSO(access_token, refresh_token)
      ```
      Upon initializing, the class fetches user information using the provided tokens.

    - **Getting New Token**:
      If an access token has expired, `get_new_token` retrieves a new one using the refresh token.
      ```python
      new_token = aol_sso_instance.get_new_token()
      ```

    - **Fetching User Information**:
      `get_user_info` fetches and returns basic user information like email, first name, and last name.
      ```python
      user_info = aol_sso_instance.get_user_info()
      ```

    - **Sending Emails**:
      Use the `send_email` method to send an email to a recipient.
      ```python
      aol_sso_instance.send_email(to="recipient@example.com", subject="Hello", message_text="This is a test email.")
      ```

4. **OAuth Flow**

    Use the `aol_sso` function to set up the OAuth flow with AOL. This function exchanges an authorization code for access and refresh tokens.

    ```python
    from aol import aol_sso

    code = "your_authorization_code_here"
    redirect_uri = "your_redirect_uri_here"  # This should match the redirect URI set in the AOL developer console
    aol_sso_instance = aol_sso(code, redirect_uri)
    ```

    Ensure that the `MAGIC_LINK_URL` environment variable is set if you do not provide the `redirect_uri` parameter.

### Example Usage

1. **Exchange Authorization Code for Tokens and Initialize AOLSSO Instance**:

    ```python
    from aol import aol_sso

    code = "your_authorization_code_here"
    redirect_uri = "your_redirect_uri_here"  # e.g., "https://yourapp.com/callback"
    aol_sso_instance = aol_sso(code, redirect_uri)

    if aol_sso_instance:
        user_info = aol_sso_instance.get_user_info()
        print(f"User Info: {user_info}")
        
        aol_sso_instance.send_email(
            to="recipient@example.com",
            subject="Test Email",
            message_text="This is a test email from AOL SSO integration."
        )
    else:
        print("Failed to authenticate with AOL.")
    ```

### Possible Issues

- Ensure that `AOL_CLIENT_ID` and `AOL_CLIENT_SECRET` are set correctly in the environment.
- The provided OAuth scopes must match the scopes set in the AOL developer console.
- Replace the hypothetical endpoints with actual endpoints provided by AOL if available.
- Error handling has been implemented to catch common issues such as token expiration and missing user info.

By following these steps, you can set up AOL SSO integration in your project to authenticate users and send emails on their behalf using AOL.