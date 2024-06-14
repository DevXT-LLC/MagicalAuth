## Foursquare SSO Integration

The following documentation will guide you through the steps necessary to set up and use Foursquare Single Sign-On (SSO) in your application.

### Required Environment Variables

Before you start, you need to have the following environment variables set in your `.env` file:

- `FOURSQUARE_CLIENT_ID`: Your Foursquare OAuth client ID.
- `FOURSQUARE_CLIENT_SECRET`: Your Foursquare OAuth client secret.

### Steps to Acquire Foursquare OAuth Credentials

To obtain the `FOURSQUARE_CLIENT_ID` and `FOURSQUARE_CLIENT_SECRET`, follow these steps:

1. **Create a Foursquare Developer Account:**
   - Go to the [Foursquare Developer Portal](https://developer.foursquare.com/).
   - Sign up or log in to your Foursquare account.

2. **Create a New App:**
   - Once logged in, go to the "My Apps" section.
   - Click on "Create a New App".
   - Fill in the required details about your application.
   - After filling in the details, submit the form to create the app.

3. **Retrieve Your Credentials:**
   - After creating the app, you will be taken to your app's details page.
   - Your `Client ID` and `Client Secret` will be displayed on this page. These are the values you need to add to your `.env` file.

### Required APIs

The basic Foursquare API does not require any specific scopes for accessing basic user information. Foursquare uses a userless access approach for its APIs.

### How to Set Up Foursquare SSO

Add the `FOURSQUARE_CLIENT_ID` and `FOURSQUARE_CLIENT_SECRET` environment variables to your `.env` file:

```env
FOURSQUARE_CLIENT_ID=your-client-id
FOURSQUARE_CLIENT_SECRET=your-client-secret
```

### Example Code

Below are examples of how to use the `FoursquareSSO` class to handle Foursquare SSO:

#### Initializing the SSO and Fetching User Info

To use this class, instantiate it with an access token. This can be obtained by the `foursquare_sso` function after the user authorizes your app.

```python
from sso.foursquare import FoursquareSSO, foursquare_sso

# Use the code obtained after user authorization and the redirect URI
code = 'authorization_code'
redirect_uri = 'https://your-redirect-uri.com'

foursquare_sso_instance = foursquare_sso(code, redirect_uri=redirect_uri)

if foursquare_sso_instance:
   user_info = foursquare_sso_instance.user_info
   print("User Info:", user_info)
```

#### Handling Unauthorized Access

If the access token is expired or invalid, the `get_user_info` method will raise an `HTTPException` with a 401 status code, prompting re-authentication.

```python
try:
    user_info = foursquare_sso_instance.get_user_info()
    print("User Info:", user_info)
except HTTPException as e:
    if e.status_code == 401:
        print("Unauthorized, please re-authenticate")
```

### Handling Access Token Retrieval

Foursquare does not have a refresh token mechanism. In case an access token expires, you will need to prompt the user to re-authenticate.

## Example

Here is a minimal example demonstrating how to set up Foursquare SSO in a FastAPI application:

```python
from fastapi import FastAPI, Request, HTTPException
from sso.foursquare import foursquare_sso

app = FastAPI()

@app.get("/login/foursquare")
async def login_with_foursquare(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    redirect_uri = "https://your-redirect-uri.com"
    sso_instance = foursquare_sso(code, redirect_uri=redirect_uri)
    
    if not sso_instance:
        raise HTTPException(status_code=500, detail="Failed to fetch access token from Foursquare")
    
    user_info = sso_instance.user_info
    return user_info
```

In this example, after the user authorizes your application, they will be redirected back to your specified `redirect_uri` with an authorization code. This code is then used to initialize the `FoursquareSSO` class and fetch the user's basic information.