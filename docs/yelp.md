## Yelp SSO Integration

The Yelp SSO integration allows users to authenticate and retrieve user information through Yelp's OAuth system. This section provides a detailed guide on how to configure and use the Yelp SSO in your application. 

### Required Environment Variables

This integration requires the following environment variables:

- `YELP_CLIENT_ID`: Yelp OAuth client ID
- `YELP_CLIENT_SECRET`: Yelp OAuth client secret

To set these variables, ensure they are included in your application's environment configuration file (e.g., `.env`):

```plaintext
YELP_CLIENT_ID=your_client_id_here
YELP_CLIENT_SECRET=your_client_secret_here
```

### Acquiring Client ID and Client Secret

To obtain the `YELP_CLIENT_ID` and `YELP_CLIENT_SECRET`, follow these steps:

1. **Register Your App:**
    - Go to the [Yelp Developer Portal](https://www.yelp.com/developers/v3/get_started).
    - Log in or create a Yelp account.
    - Navigate to the "Create App" section.
    - Fill out the required details to register your application.

2. **Retrieve Credentials:**
    - Once your application is registered, you will be provided with a `CLIENT_ID` and `CLIENT_SECRET`.

### Required Scopes

Ensure your application requests the necessary scopes for Yelp OAuth:

- `business`

These scopes allow the application to access specific user information and perform operations permitted by Yelp's API.

### Usage

Here is a step-by-step guide on how to use the Yelp SSO integration:

1. **Initialize YelpSSO:**
    - Create an instance of `YelpSSO` class with the access token and refresh token.

    ```python
    from sso.yelp import YelpSSO

    yelp_sso_instance = YelpSSO(access_token="your_access_token", refresh_token="your_refresh_token")
    ```

2. **Retrieve User Information:**
    - Access the user's information using the `user_info` attribute of the `YelpSSO` instance.

    ```python
    user_info = yelp_sso_instance.user_info
    print(user_info)
    ```

3. **Handle Token Refresh:**
    - The `YelpSSO` class automatically handles token refresh if the access token expires.

### Example Code for Initializing Yelp SSO

Below is an example of how to initialize Yelp SSO after acquiring an authorization code:

```python
from sso.yelp import yelp_sso

# Assume 'auth_code' is obtained from Yelp's OAuth redirect
auth_code = "received_authorization_code"
redirect_uri = "your_redirect_uri"

try:
    yelp_instance = yelp_sso(code=auth_code, redirect_uri=redirect_uri)
    user_info = yelp_instance.user_info
    print("User Info:", user_info)
except HTTPException as e:
    print(f"Error: {e.detail}")
```

In the above implementation:
- Replace `received_authorization_code` with the actual authorization code you receive from Yelp's OAuth flow.
- Replace `your_redirect_uri` with the redirect URI configured in Yelp's OAuth system.

### Additional Considerations

- **Sending Email:** The `send_email` method is not implemented for Yelp SSO as the Yelp API does not support sending emails directly.
- **Error Handling:** Ensure to handle HTTP exceptions properly to manage errors related to token acquisition or user information retrieval.

By following these instructions, you will be able to set up and use the Yelp SSO integration in your application effectively.