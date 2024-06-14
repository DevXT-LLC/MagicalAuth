## WSO2 Identity Single Sign-On (SSO) Documentation

This guide provides detailed instructions on how to set up and configure WSO2 Identity Server for Single Sign-On (SSO) in your application. The provided `wso2_identity.py` script allows you to authenticate users and send emails via WSO2 Identity Server.

### Required Environment Variables

To use the provided script, you need to set up the following environment variables:

- `WSO2_CLIENT_ID`: The OAuth client ID obtained from WSO2 Identity Server
- `WSO2_CLIENT_SECRET`: The OAuth client secret obtained from WSO2 Identity Server

### Required APIs

Make sure you have the necessary APIs enabled within your WSO2 Identity Server. Add the `WSO2_CLIENT_ID` and `WSO2_CLIENT_SECRET` environment variables to your `.env` file.

### Required Scopes for WSO2 SSO

- `openid`
- `profile`
- `email`
- `wso2.send_email` (assuming WSO2 has a custom scope for sending emails)

The permissions granted by these scopes will allow your application to access basic user profile information and send emails on behalf of the user.

### Example Usage

Below is a step-by-step guide on how to set up your environment and use the `WSO2SSO` class for authentication and email sending:

#### Step 1: Acquire WSO2 OAuth Client ID and Secret

1. **Access the WSO2 Identity Server Management Console:**
   - Typically, you can access it at `https://<your-wso2-server>/carbon`.

2. **Create an OAuth Client:**
   - Navigate to the OAuth/OpenID Connect section.
   - Register a new OAuth application.
   - Obtain the `Client ID` and `Client Secret`.

3. **Configure the OAuth Application:**
   - Set the Authorized Redirect URIs.
   - Ensure the required scopes (`openid`, `profile`, `email`, and `wso2.send_email`) are configured.

#### Step 2: Set Environment Variables

Add the `WSO2_CLIENT_ID` and `WSO2_CLIENT_SECRET` to your `.env` file:

```plaintext
WSO2_CLIENT_ID=your-wso2-client-id
WSO2_CLIENT_SECRET=your-wso2-client-secret
MAGIC_LINK_URL=your-redirect-uri
```

Ensure the `.env` file is placed in the root of your project directory for the script to access these variables.

#### Step 3: Implement the WSO2 SSO in Your Project

The sample code provided will help you get started:

1. **Authenticate Users:**
   - The `wso2_identity_sso` function handles the authentication process and retrieves access and refresh tokens.

   ```python
   from wso2_identity import wso2_identity_sso

   code = "authorization-code-from-wso2"
   wso2_sso_instance = wso2_identity_sso(code)
   
   if wso2_sso_instance:
       print("Access Token:", wso2_sso_instance.access_token)
       print("User Info:", wso2_sso_instance.user_info)
   ```

2. **Send Email Using WSO2:**
   - The `send_email` method in the `WSO2SSO` class sends an email using the WSO2 email sending endpoint.

   ```python
   subject = "Test Email"
   message_text = "This is a test email using WSO2."
   to = "recipient@example.com"

   try:
       response = wso2_sso_instance.send_email(to, subject, message_text)
       print("Email sent successfully:", response)
   except HTTPException as e:
       print("An error occurred:", e.detail)
   ```

#### Step 4: Handling Token Refresh
The `WSO2SSO` class includes methods to automatically refresh the access token if it has expired, ensuring seamless user authentication.

#### Additional Configuration
- **Logging:** The script logs errors and responses to assist in debugging any issues that may arise during the authentication or email sending processes.
  
### Final Notes
Ensure that all relevant APIs are enabled on the WSO2 Identity Server and the necessary scopes are granted. Properly configure your `.env` file with all the required environment variables before executing the script.

By following these instructions, you will be able to integrate WSO2 Identity Server SSO into your application, enabling OAuth-based user authentication and email sending capabilities.