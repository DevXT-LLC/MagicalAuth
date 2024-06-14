## Zendesk SSO Integration Guide

This guide provides detailed instructions to integrate Zendesk Single Sign-On (SSO) into your application using the provided `zendesk.py` script. By following these steps, you will set up the necessary environment variables, OAuth client, and required OAuth scopes to enable seamless authentication and email sending through Zendesk.

### Required Environment Variables

Before you proceed with the Zendesk integration, ensure that you have the following environment variables set up in your `.env` file:

- `ZENDESK_CLIENT_ID`: Your Zendesk OAuth client ID
- `ZENDESK_CLIENT_SECRET`: Your Zendesk OAuth client secret
- `ZENDESK_SUBDOMAIN`: Your Zendesk subdomain (e.g., if your Zendesk URL is `https://yourcompany.zendesk.com`, then your subdomain is `yourcompany`)

### Acquiring the Required Keys

To acquire the required keys for setting up the environment variables:

1. **Create a Zendesk OAuth Client:**
   - Log in to your Zendesk Admin Center.
   - Navigate to `Channels` > `API`.
   - Under the `OAuth Clients` tab, click on the `Add OAuth Client` button.
   - Fill in the required details:
     - **Client Name:** A recognizable name for your OAuth client.
     - **Description:** A brief description for your reference.
     - **Client ID:** This will be automatically generated. Copy this value.
     - **Client Secret:** Click the `Reveal` button to see the client secret. Copy this value too.
     - **Redirect URLs:** Add the URL(s) where Zendesk will redirect after an authentication attempt.
   - Save your new OAuth client.

2. **Set the environment variables**:
   Add the following lines to your `.env` file:
   ```
   ZENDESK_CLIENT_ID=your_zendesk_client_id
   ZENDESK_CLIENT_SECRET=your_zendesk_client_secret
   ZENDESK_SUBDOMAIN=your_zendesk_subdomain
   ```

### Required APIs

Make sure the following APIs are enabled in your Zendesk account:

- OAuth API for authentication and token exchange.
- Users API to retrieve user information.
- Requests API to handle support requests and send emails.

### Required Scopes for Zendesk OAuth

When you set up your OAuth client, ensure that the following scopes are enabled:

- `read`: To grant read access.
- `write`: To grant write access.

### Example Usage

Here is an example of how to use the `zendesk.py` script:

1. **Initialize the OAuth Flow:**
   ```python
   from sso.zendesk import zendesk_sso

   # Assuming you have an authorization code from Zendesk
   auth_code = "authorization_code_from_zendesk"
   magic_link_url = "your_magic_link_url"  # Optional; can use the one set in the environment

   zendesk_sso_instance, error = zendesk_sso(auth_code, redirect_uri=magic_link_url)
   if error:
       print("Error during SSO:", error)
   else:
       print("SSO successful:", zendesk_sso_instance.user_info)
   ```

2. **Send an Email:**
   ```python
   subject = "Test Subject"
   message_text = "Test email body"
   recipient_email = "recipient@example.com"

   response = zendesk_sso_instance.send_email(to=recipient_email, subject=subject, message_text=message_text)
   print("Email sent response:", response)
   ```

Make sure to replace the placeholders with actual values related to your Zendesk setup.

### Error Handling

The script includes basic error handling to manage authentication failures and API call issues. If the initial token exchange fails, it will attempt to refresh the token and retry the operation.

Ensure that you have enabled all necessary permissions and configured the correct environment variables for seamless integration with Zendesk.

By following this guide, you should be able to quickly and easily set up your Zendesk SSO and handle user authentication and email sending within your application.