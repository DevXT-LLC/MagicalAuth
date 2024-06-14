Certainly! Below is the detailed documentation for setting up and using the Viadeo Single Sign-On (SSO) functionality. The documentation follows the example format provided.

## Viadeo

### Required environment variables

- `VIADEO_CLIENT_ID`: Viadeo OAuth client ID
- `VIADEO_CLIENT_SECRET`: Viadeo OAuth client secret

### Required APIs

Ensure you have the required APIs enabled, then add the `VIADEO_CLIENT_ID` and `VIADEO_CLIENT_SECRET` environment variables to your `.env` file.

To acquire the `VIADEO_CLIENT_ID` and `VIADEO_CLIENT_SECRET`, follow these steps:

1. **Creating an App on Viadeo:**
   - Navigate to the [Viadeo Developer Portal](https://developer.viadeo.com/).
   - Sign in with your Viadeo account.
   - Create a new application and provide the necessary details.
   - Upon creation, you will be issued a `Client ID` and `Client Secret`.

2. **Setting Up Environment Variables:**
   - After obtaining the `Client ID` and `Client Secret`, add these values to your `.env` file:
     ```plaintext
     VIADEO_CLIENT_ID=your_client_id_here
     VIADEO_CLIENT_SECRET=your_client_secret_here
     ```

### Required Scopes for Viadeo OAuth

- `basic` (to access user profile)
- `email` (to access user email)

### Example Usage

When incorporating Viadeo SSO into your application, it will allow users to authenticate using their Viadeo account and enable various functionalities like fetching user information and sending emails.

For instance:

```python
from fastapi import FastAPI, Request
from .sso.viadeo import viadeo_sso

app = FastAPI()

@app.get("/login_viadeo")
async def login_viadeo(request: Request, code: str):
    redirect_uri = "YOUR_REDIRECT_URI"
    viadeo_user = viadeo_sso(code, redirect_uri)
    if not viadeo_user:
        return {"error": "Failed to authenticate with Viadeo."}

    user_info = viadeo_user.user_info
    return user_info

@app.post("/send_email")
async def send_email(request: Request, to: str, subject: str, message: str):
    # Assuming you have already authenticated via Viadeo SSO and have the token
    viadeo_user = viadeo_sso(CODE_FROM_AUTH_FLOW)
    if not viadeo_user:
        return {"error": "User not authenticated."}

    response = viadeo_user.send_email(to, subject, message)
    if "error" in response:
        return {"error": "Failed to send email."}

    return {"message": "Email sent successfully!"}
```

### Functions

#### `viadeo_sso(code, redirect_uri=None) -> ViadeoSSO`
- **Parameters:**
  - `code`: The authorization code received from Viadeo after the user grants permission.
  - `redirect_uri`: The URI to redirect to after authentication (default is fetched from environment variable `MAGIC_LINK_URL`).
- **Returns:** A `ViadeoSSO` instance with authenticated details or `None` if authentication fails.

#### `ViadeoSSO.get_user_info()`
- **Function:** Fetches the authenticated user's profile information.
- **Returns:** A dictionary containing `email`, `first_name`, and `last_name`.

#### `ViadeoSSO.send_email(to, subject, message_text)`
- **Function:** Sends an email using the Viadeo API.
- **Parameters:**
  - `to`: Recipient's email address.
  - `subject`: Subject of the email.
  - `message_text`: Body content of the email.
- **Returns:** A response dictionary from the Viadeo API.

### Notes

- Ensure to handle errors and exceptions gracefully.
- Confirm Viadeo API response formats by referring to the [Viadeo API documentation](https://developer.viadeo.com/).
- Update your `.env` file with the necessary environment variables for seamless operation.

By following this documentation, you will be able to integrate Viadeo SSO into your application effectively, allowing users to authenticate and interact through their Viadeo accounts.