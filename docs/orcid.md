## ORCID

### Required Environment Variables

To set up ORCID Single Sign-On (SSO), you will need the following environment variables:

- `ORCID_CLIENT_ID`: ORCID OAuth client ID
- `ORCID_CLIENT_SECRET`: ORCID OAuth client secret

### How to Acquire ORCID Client ID and Secret

1. **Register your application with ORCID**: If you haven't already, you need to register your application with ORCID. Visit the [ORCID Developer Tools](https://orcid.org/content/register-client-application).

2. **Fill out the registration form**: Provide necessary details about your application. After the registration is complete, you will receive your `ORCID_CLIENT_ID` and `ORCID_CLIENT_SECRET`.

3. **Add environment variables**: Once you have your `ORCID_CLIENT_ID` and `ORCID_CLIENT_SECRET`, add them to your `.env` file as follows:

    ```plaintext
    ORCID_CLIENT_ID=your_orcid_client_id
    ORCID_CLIENT_SECRET=your_orcid_client_secret
    ```

### Required Scopes for ORCID SSO

The following scopes are required for ORCID SSO:

- `/authenticate`: This scope allows the application to read public profile information.
- `/activities/update` (optional): This scope allows the application to update ORCID activities.

### Example: ORCIDSSO Usage

The `ORCIDSSO` class in the example above handles the OAuth token exchange and retrieves user information from ORCID. Here is how you can use it:

1. **Authorize with ORCID**: Direct the user to ORCID for authorization. Once the user authorizes your application, ORCID will redirect them back to your application with an authorization `code`.

2. **Exchange Authorization Code for Tokens**: Use the `orcid_sso` function to exchange the authorization code for access and refresh tokens.

    ```python
    from sso.orcid import orcid_sso

    code = "your_authorization_code"
    redirect_uri = "https://your-app.com/callback"

    orcid_sso_instance, error = orcid_sso(code, redirect_uri)

    if orcid_sso_instance:
        user_info = orcid_sso_instance.user_info
        print(user_info)
    else:
        print(f"Error: {error}")
    ```

### Required APIs for ORCID SSO

No specific APIs need to be enabled for ORCID integration, but you must ensure the `ORCID_CLIENT_ID` and `ORCID_CLIENT_SECRET` environment variables are correctly set up.

### Additional Information

- **Documentation**: For more detailed information on ORCID OAuth, refer to the [ORCID API Documentation](https://members.orcid.org/api).
- **Testing**: To test your ORCID SSO setup, you can use the ORCID sandbox environment, which allows you to create test accounts and client applications. Visit the [ORCID Sandbox](https://sandbox.orcid.org/) for more information.

By following the steps and guidelines above, you can set up ORCID SSO quickly and easily, enabling secure and authenticated access to ORCID user data in your application.