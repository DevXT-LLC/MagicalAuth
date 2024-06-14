## OpenAM SSO

### Overview

This module provides Single Sign-On (SSO) functionality using OpenAM's OAuth 2.0 service. It enables users to obtain tokens and user information from OpenAM, and also provides a mechanism for token refresh.

### Required Environment Variables

To use the OpenAM SSO module, you must set the following environment variables:

- `OPENAM_CLIENT_ID`: OpenAM OAuth client ID
- `OPENAM_CLIENT_SECRET`: OpenAM OAuth client secret
- `OPENAM_BASE_URL`: Base URL for the OpenAM server (e.g., "https://openam.example.com")

### Required Scopes for OpenAM OAuth

The following scopes are required for OpenAM OAuth:

- `profile`
- `email`

### Instructions to Acquire Keys and Set Up Environment Variables

1. **Register the Client with OpenAM:**
   
   - **Navigate to Admin Console:** Log in to the OpenAM administrative console.
   - **Register the Application:**
     - Go to `Applications` > `Agents` > `OAuth 2.0 / OIDC` > `Clients`.
     - Click `New Client`.
     - Fill in details such as `Client ID`, `Client Secret`, and `Redirect URIs`.
   - **Set Scopes:**
     - Ensure that your client has the required scopes (`profile` and `email`).

2. **Obtain Client ID and Secret:**
   
   - **Client ID**: Found in the client registration under OpenAM's administrative console.
   - **Client Secret**: Found in the client registration under OpenAM's administrative console.

3. **Set Environment Variables:**

   Add the obtained values to your environment file (`.env`).

   ```
   OPENAM_CLIENT_ID=<your_openam_client_id>
   OPENAM_CLIENT_SECRET=<your_openam_client_secret>
   OPENAM_BASE_URL=<your_openam_base_url>
   ```

### Usage Example

Here's an example of how to use the OpenAMSSO class:

```python
from sso.openam import OpenAMSSO, openam_sso
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/openam_callback")
async def openam_callback(request: Request):
    code = request.query_params.get('code')
    if code is None:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    openam_sso_instance, error = openam_sso(code)
    if error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")

    user_info = openam_sso_instance.user_info
    return {
        "email": user_info["email"],
        "first_name": user_info["first_name"],
        "last_name": user_info["last_name"],
    }
```

### Error Handling

- If the access token is expired or invalid, the `get_user_info` method will automatically attempt to obtain a new one using the refresh token.
- In case of an error retrieving user information, an HTTPException with a detailed message will be raised.

### Extensions

Currently, the `send_email` method is not implemented, as OpenAM does not provide support for sending emails by default. This method raises a `NotImplementedError` when called. Ensure your usage of the class accounts for this limitation.

By following these instructions and ensuring all required environment variables and scopes are correctly set, you should be able to implement OpenAM SSO functionality without any issues.