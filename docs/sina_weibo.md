# Sina Weibo Single Sign-On (SSO) Integration

## Overview

This module enables Single Sign-On (SSO) integration with Sina Weibo through OAuth 2.0. This guide provides the necessary steps and details to set up the integration, including acquiring the required keys, setting up environment variables, and implementing the code provided.

## Required Environment Variables

In order to use the Sina Weibo SSO integration, you need to set several environment variables. These variables are used in the OAuth authentication process to communicate with the Weibo API. 

Below is a list of the required environment variables:

- `WEIBO_CLIENT_ID`: Weibo OAuth client ID
- `WEIBO_CLIENT_SECRET`: Weibo OAuth client secret
- `MAGIC_LINK_URL`: Your application's redirect URL used in the OAuth process

## Required APIs and Scopes

Before proceeding, ensure you have the necessary APIs enabled and permissions configured. The required scopes for Weibo OAuth are:

- `email`
- `statuses_update`

## Steps to Acquire Keys and Set Up Environment

### Step 1: Register Your Application with Weibo

1. Log in to the [Weibo Open Platform](https://open.weibo.com/).
2. Navigate to "My Apps" and click on "Create App".
3. Fill in the required details about your application, such as name, description, and redirect URL.
4. Once your application is created, you will receive a `CLIENT_ID` and `CLIENT_SECRET`.

### Step 2: Set Up Your Environment Variables

Once you have your `CLIENT_ID` and `CLIENT_SECRET`, you'll need to add them to your environment as follows:

1. Create a `.env` file in the root directory of your project.
2. Add the following lines to your `.env` file:

```
WEIBO_CLIENT_ID=your_client_id
WEIBO_CLIENT_SECRET=your_client_secret
MAGIC_LINK_URL=your_redirect_uri
```

Replace `your_client_id`, `your_client_secret`, and `your_redirect_uri` with your actual Weibo OAuth credentials and your application's redirect URL.

## Usage

Here is an overview of the provided code and how you can use it to integrate Weibo OAuth into your application.

### WeiboSSO Class

The `WeiboSSO` class encapsulates the logic for authenticating with Weibo, refreshing tokens, fetching user information, and sending messages (statuses). 

#### Constructor
The constructor initializes the `WeiboSSO` instance with access and refresh tokens, fetching user information upon initialization.

```python
def __init__(
    self,
    access_token=None,
    refresh_token=None,
):
    self.access_token = access_token
    self.refresh_token = refresh_token
    self.client_id = getenv("WEIBO_CLIENT_ID")
    self.client_secret = getenv("WEIBO_CLIENT_SECRET")
    self.user_info = self.get_user_info()
```

#### Methods

1. **get_new_token**: Refreshes the access token using the Weibo API.

    ```python
    def get_new_token(self):
        response = requests.post(
            "https://api.weibo.com/oauth2/access_token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
        )
        return response.json()["access_token"]
    ```

2. **get_user_info**: Fetches the user's information such as `email` and `first_name`.

    ```python
    def get_user_info(self):
        uri = "https://api.weibo.com/2/account/get_uid.json"
        response = requests.get(
            uri,
            params={"access_token": self.access_token},
        )
        if response.status_code == 401:
            self.access_token = self.get_new_token()
            response = requests.get(
                uri,
                params={"access_token": self.access_token},
            )
        try:
            uid_response = response.json()
            uid = uid_response["uid"]

            uri_info = f"https://api.weibo.com/2/users/show.json?uid={uid}"
            response = requests.get(
                uri_info,
                params={"access_token": self.access_token},
            )
            data = response.json()
            email = data.get("email", None)
            first_name = data["name"]
            last_name = ""
            return {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        except:
            raise HTTPException(
                status_code=400,
                detail="Error getting user info from Weibo",
            )
    ```

3. **send_message**: Posts a status update to the user's Weibo account.

    ```python
    def send_message(self, status):
        uri = "https://api.weibo.com/2/statuses/update.json"
        data = {
            "access_token": self.access_token,
            "status": status,
        }

        response = requests.post(
            uri,
            data=data,
        )

        if response.status_code == 401:
            self.access_token = self.get_new_token()
            data["access_token"] = self.access_token
            response = requests.post(
                uri,
                data=data,
            )
        return response.json()
    ```

### sina_weibo_sso Function

The `sina_weibo_sso` function initializes and returns a `WeiboSSO` instance. This function handles the OAuth process, exchanges the authorization code for access and refresh tokens, and returns an initialized `WeiboSSO` object.

```python
def sina_weibo_sso(code, redirect_uri=None) -> WeiboSSO:
    if not redirect_uri:
        redirect_uri = getenv("MAGIC_LINK_URL")
    code = (
        str(code)
        .replace("%2F", "/")
        .replace("%3D", "=")
        .replace("%3F", "?")
        .replace("%3D", "=")
    )
    response = requests.post(
        f"https://api.weibo.com/oauth2/access_token",
        data={
            "client_id": getenv("WEIBO_CLIENT_ID"),
            "client_secret": getenv("WEIBO_CLIENT_SECRET"),
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    if response.status_code != 200:
        logging.error(f"Error getting Weibo access token: {response.text}")
        return None, None
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"] if "refresh_token" in data else "Not provided"
    return WeiboSSO(access_token=access_token, refresh_token=refresh_token)
```

## Conclusion

Follow the steps outlined in this guide to set up and integrate Sina Weibo SSO into your application. After configuring the environment variables and implementing the provided code, you should be able to authenticate users via Weibo, fetch their information, and post status updates on their behalf.