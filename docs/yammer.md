## Yammer Integration

This module provides Single Sign-On (SSO) and messaging capabilities using Yammer's OAuth 2.0. It allows a user to authenticate via Yammer, acquire an access token, retrieve user information, and send messages to Yammer groups.

### Prerequisites

Before you can use this module, you need to set up a few things on Yammer and obtain the necessary credentials. Here is a step-by-step guide to help you:

### Step-by-Step Guide

1. **Creating a Yammer App:**
    - Go to the [Yammer Developer Site](https://www.yammer.com/client_applications)
    - Click on "Register New App".
    - Fill out the form with the required details such as:
        - **App Name**
        - **Organization**
        - **Support Email**
    - In the "Redirect URL" field, enter the URL where users will be redirected after authentication (usually your application's URL).

2. **Obtaining the Client ID and Client Secret:**
    - After creating your app, you will be taken to the app details page.
    - Here, you will find your **Client ID** and **Client Secret**. 

3. **Environment Configuration:**
    - Create a `.env` file in your project root directory if you don't already have one.
    - Add the following environment variables to your `.env` file:
      ```plaintext
      YAMMER_CLIENT_ID=your_yammer_client_id
      YAMMER_CLIENT_SECRET=your_yammer_client_secret
      ```

### Required APIs

Make sure to enable the following Yammer API scopes:
- `messages:email`
- `messages:post`
  
These scopes can be configured when registering your app on the Yammer developer site.

### Using the Module

Here's a brief guide on how to use the `YammerSSO` class and associated functions.

#### Initialize SSO and Retrieve User Info:

```python
from sso.yammer import yammer_sso

# Authentication and getting YammerSSO instance
code = "authorization_code_you_received"
redirect_uri = "your_redirect_url"

yammer_instance = yammer_sso(code, redirect_uri)

# Get user information
user_info = yammer_instance.user_info
print(user_info)
```

#### Send a Message:

```python
group_id = "your_yammer_group_id"
message_text = "Hello, Yammer!"

# Send message to a Yammer group
response = yammer_instance.send_message(group_id, message_text)
print(response)
```

### Error Handling

- **HTTP 401 Unauthorized:** 
  - If your access token is expired or invalid, the module will attempt to refresh it using the refresh token.
- **HTTP 400 Bad Request:**
  - If there is an error in getting user information or sending messages, an `HTTPException` is raised.

### Example

```python
import os
from sso.yammer import yammer_sso

def main():
    try:
        # Assuming you've already set up your environment variables
        code = os.getenv('AUTHORIZATION_CODE')
        redirect_uri = os.getenv('REDIRECT_URI')
        yammer_instance = yammer_sso(code, redirect_uri)
        
        # Print user information
        user_info = yammer_instance.user_info
        print(f"User Info: {user_info}")

        # Send a message to a group
        group_id = "123456"
        message = "Hello from Python!"
        response = yammer_instance.send_message(group_id, message)
        print(f"Message sent response: {response}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

### Note:
- Update the `YAMMER_CLIENT_ID`, `YAMMER_CLIENT_SECRET`, and other configurable parameters as per your settings.

By following these guidelines, you should be able to set up and use the Yammer SSO and messaging functionalities smoothly. For any advanced configurations and additional capabilities, refer to the [Yammer SDK Documentation](https://developer.yammer.com/docs/).