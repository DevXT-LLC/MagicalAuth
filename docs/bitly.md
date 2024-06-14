## Bitly Integration

The Bitly integration allows you to shorten URLs and manage Bitly tokens using the Bitly API.

### Required Environment Variables

- `BITLY_CLIENT_ID`: Bitly OAuth client ID
- `BITLY_CLIENT_SECRET`: Bitly OAuth client secret
- `BITLY_ACCESS_TOKEN`: Bitly access token (you can obtain it via OAuth or from the Bitly account settings)

### Required Scopes for Bitly OAuth

- `bitly:read`
- `bitly:write`

### How to Acquire Required Keys and Tokens

1. **Create a Bitly Account**:
   - Sign up for a Bitly account at https://bitly.com/.

2. **Create an OAuth App**:
   - Navigate to https://app.bitly.com/settings/integrations/.
   - Click on "Registered OAuth Apps" and then "Add a New App".
   - Fill in the required information to create a new app. The "App Name" and "App Description" can be anything, but for "Redirect URIs," you'll need to specify the URIs that Bitly will redirect to after authentication.
   - After creating the app, you will receive a `Client ID` and `Client Secret`.

3. **Generate an Access Token**:
   - You can generate an access token from your Bitly account settings.
   - Go to https://app.bitly.com/settings/api/, and click on "Generic Access Token" to create a new token. 

4. **Set up Environment Variables**:
   - Add the following environment variables to your `.env` file:
     ```plaintext
     BITLY_CLIENT_ID=your_bitly_client_id
     BITLY_CLIENT_SECRET=your_bitly_client_secret
     BITLY_ACCESS_TOKEN=your_bitly_access_token
     ```

### Using the Bitly Class

The `Bitly` class in your application allows you to shorten URLs and refresh the access token if needed.

#### Shortening a URL

To shorten a URL, you can use the `shorten_url` method of the `Bitly` class:

```python
from bitly import Bitly

bitly_client = Bitly()
short_url = bitly_client.shorten_url("https://example.com/your-long-url")
print(short_url)
```

#### Refreshing Token

The `get_new_token` method in the `Bitly` class will automatically handle token refreshing when the access token expires.

### Using the `bitly_sso` Function

The `bitly_sso` function helps you handle the Bitly Single Sign-On (SSO) flow, which authenticates users and gets new access and refresh tokens.

```python
from bitly import bitly_sso

code = "your-bitly-auth-code"
redirect_uri = "your-redirect-uri"
bitly_instance, refresh_token = bitly_sso(code, redirect_uri=redirect_uri)

# Use the bitly_instance to perform actions
short_url = bitly_instance.shorten_url("https://example.com/your-long-url")
print(short_url)
```

In the `bitly_sso` function, Bitly exchanges a `code` received after user authentication for an access token. If no `redirect_uri` is specified, it will default to the `MAGIC_LINK_URL` environment variable.

### Example Use Case

Here is how you might integrate the whole process in your application:

```python
from fastapi import FastAPI, HTTPException
from Globals import getenv
from bitly import bitly_sso

app = FastAPI()

@app.get("/shorten")
def shorten_url_handler(long_url: str, code: str):
    redirect_uri = getenv("MAGIC_LINK_URL")
    bitly_instance, refresh_token = bitly_sso(code, redirect_uri)
    if not bitly_instance:
        raise HTTPException(status_code=400, detail="Bitly SSO failed")
    
    try:
        short_url = bitly_instance.shorten_url(long_url)
        return {"short_url": short_url}
    except HTTPException as e:
        return {"error": str(e)}
```

With the above setup, you enable users to shorten URLs using Bitly while handling authentication and token management seamlessly.