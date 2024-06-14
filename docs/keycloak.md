## Keycloak Single Sign-On (SSO) Integration

This script facilitates Single Sign-On (SSO) integration with Keycloak by enabling seamless user authentication and retrieval of user information using OAuth 2.0.

### Required Environment Variables

Before running the `keycloak.py` script, ensure you have the following environment variables set up:

- `KEYCLOAK_CLIENT_ID`: Keycloak OAuth client ID
- `KEYCLOAK_CLIENT_SECRET`: Keycloak OAuth client secret
- `KEYCLOAK_REALM`: Name of the Keycloak realm
- `KEYCLOAK_SERVER_URL`: Base URL of the Keycloak server

These variables can typically be added to your `.env` file.

### Required Scopes for Keycloak SSO

- `openid`
- `email`
- `profile`

### Example Usage

1. **Acquire Keycloak OAuth Client Credentials:**

   - **Client ID and Client Secret:**
     1. Log in to your Keycloak admin console.
     2. Navigate to the realm where your application resides.
     3. Go to `Clients` and select the client application.
     4. Copy the `Client ID`.
     5. Go to the `Credentials` tab and copy the `Client Secret`.
   
   - **Realm:**
     1. Your Keycloak realm name should be visible in the Keycloak admin console, typically displayed near the top-left after logging in.
   
   - **Server URL:**
     1. Your Keycloak server URL is the base URL where your Keycloak instance is hosted (e.g., `http://localhost:8080` or your deployed server URL).

2. **Add these environment variables to your `.env` file:**

   ```env
   KEYCLOAK_CLIENT_ID=your_keycloak_client_id
   KEYCLOAK_CLIENT_SECRET=your_keycloak_client_secret
   KEYCLOAK_REALM=your_keycloak_realm
   KEYCLOAK_SERVER_URL=your_keycloak_server_url
   ```

3. **Include necessary dependencies:**

   Ensure you have FastAPI and request libraries added to your project:
   ```bash
   pip install fastapi requests python-dotenv
   ```

4. **Create an instance of `KeycloakSSO`:**

   Here is how you can use the `KeycloakSSO` class:
   
   ```python
   from sso.keycloak import keycloak_sso

   # Example usage of the keycloak_sso function
   code = "authorization_code_received_from_keycloak"
   redirect_uri = "your_redirect_uri"  # Optional
   
   keycloak_instance, user_info = keycloak_sso(code, redirect_uri)
   if keycloak_instance:
       print(f"Access Token: {keycloak_instance.access_token}")
       print(f"User Info: {keycloak_instance.user_info}")
   else:
       print("An error occurred with Keycloak SSO")
   ```

5. **Handling Tokens and User Information:**

   The `get_user_info` method allows you to retrieve user information such as email, first name, and last name. If the access token expires, it will refresh automatically using the refresh token.

### Additional Notes

- The error handling in this script ensures that if the user details cannot be fetched due to an expired token, it will attempt to refresh the token automatically.
- Ensure the redirect URI is correctly configured in your Keycloak client settings to match the `redirect_uri` used in your application.

With this setup, you should be able to authenticate users via Keycloak and retrieve relevant profile information seamlessly. Follow the steps above accurately to avoid any misconfigurations.