## OpenStreetMap SSO Integration

This guide explains how to integrate OpenStreetMap Single Sign-On (SSO) using OAuth. Follow the steps below to acquire the required keys and set up the necessary environment variables for OpenStreetMap SSO. 

### Required Environment Variables

- `OSM_CLIENT_ID`: OpenStreetMap OAuth client ID
- `OSM_CLIENT_SECRET`: OpenStreetMap OAuth client secret

### Steps to Acquire OpenStreetMap OAuth Credentials

1. **Create an OpenStreetMap OAuth Application:**
   
   - Navigate to the [OpenStreetMap OAuth settings page](https://www.openstreetmap.org/user/{your_username}/oauth_clients).
   - Log in with your OpenStreetMap account if you are not already logged in.
   - Click on "Register your application".
   - Fill out the form with the required information:
     - **Name:** Give your application a name.
     - **Main Application URL:** Provide the URL where your application is hosted.
     - **Callback URL:** Provide the URL where the user will be redirected after authentication.
     - **Support URL:** Provide the URL for support.
   - Click the "Save" button.

2. **Save Your OAuth Credentials:**

   - After registering your application, you will be given a **client ID** and **client secret**. Keep these credentials safe.
   - Add them to your `.env` file as follows:
     ```
     OSM_CLIENT_ID=your_openstreetmap_client_id
     OSM_CLIENT_SECRET=your_openstreetmap_client_secret
     ```

### Required APIs

Ensure you have the appropriate OAuth configuration in OpenStreetMap and that the `OSM_CLIENT_ID` and `OSM_CLIENT_SECRET` environment variables are properly set in your `.env` file.

### Required Scopes for OpenStreetMap OAuth

The required scope for OpenStreetMap OAuth integration is:

- `read_prefs`

### How to Use the `openstreetmap_sso` Function

The `openstreetmap_sso` function is designed to facilitate the OAuth token exchange process and provide an authenticated session. Below is an example of how to use this function:

```python
from sso.openstreetmap import openstreetmap_sso

# Assuming you have received an authorization code
authorization_code = 'received_authorization_code_here'
redirect_uri = 'your_redirect_uri'

# Initialize OpenStreetMap SSO
openstreetmap_session = openstreetmap_sso(authorization_code, redirect_uri)

# Access user info
user_info = openstreetmap_session.user_info
print(user_info)
```

### Example

The following code snippet demonstrates how to use the OpenStreetMapSSO class and the `openstreetmap_sso` function within your application context:

```python
# main.py
from fastapi import FastAPI, Request, Depends
from sso.openstreetmap import openstreetmap_sso

app = FastAPI()

@app.get("/login/openstreetmap")
async def login_with_osm(code: str, request: Request):
    redirect_uri = str(request.url_for("login_with_osm"))
    osm_sso = openstreetmap_sso(code, redirect_uri)
    if osm_sso:
        user_info = osm_sso.user_info
        return {"user": user_info}
    else:
        return {"error": "Failed to authenticate with OpenStreetMap"}
```

In this example, when the `/login/openstreetmap` endpoint is accessed with an authorization code, it uses the `openstreetmap_sso` function to exchange the code for an access token and fetch user information.

By following the instructions provided, you should be able to successfully integrate OpenStreetMap SSO into your application.