# Jive SSO Integration

This document provides a detailed guide on integrating Jive Single Sign-On (SSO) with your application. By following these instructions, you will be able to set up environment variables and acquire the necessary OAuth keys for Jive.

## Prerequisites

Before you begin, ensure that you have the following prerequisites:

- A Jive account with the necessary permissions to create an OAuth application.
- Access to your Jive instance to perform API operations.
- Python environment set up with necessary libraries, including `requests` and `fastapi`.

## Required Environment Variables

Set up the following environment variables in your `.env` file or environment management system. These variables will be used for OAuth authentication with Jive.

- `JIVE_CLIENT_ID`: Jive OAuth client ID.
- `JIVE_CLIENT_SECRET`: Jive OAuth client secret.

## How to Acquire Jive OAuth Keys

1. **Log in to your Jive instance.**

2. **Navigate to the OAuth section:**
   - Go to `Admin Console > System > Settings > OAuth`.

3. **Create a new OAuth application:**
   - Click on "Register a New Application".
   - Fill out the application form with relevant information:
     - **Application Name**: Choose a name for your application.
     - **Client ID**: This will be provided by the system once you register the application.
     - **Client Secret**: This will also be provided by the system upon registering the application.
     - **Redirect URI**: Enter the URL where users will be redirected after authentication. This is typically your application's URL.
     - **Scopes**: Select the scopes your application will require as per Jive's API documentation.
       - Example Scopes: `read`, `write`, `admin`, etc.

4. **Save the application:**
   - Once you save the application, the `Client ID` and `Client Secret` will be generated. Note these down as you will need them for your environment variables.

5. **Add environment variables:**
   - Add the `JIVE_CLIENT_ID` and `JIVE_CLIENT_SECRET` to your `.env` file or manage them in your service's environment configuration.

## Required APIs

Ensure you have the necessary Jive API enabled to perform operations such as fetching user information and sending emails.

## Required Scopes for Jive OAuth

The required scopes for Jive OAuth will depend on what operations you wish to perform. Commonly used scopes include:

- **Read**: To read user information.
- **Write**: To send emails or perform other writing operations.
- **Admin**: For administrative tasks.

Refer to Jive’s API documentation for a detailed list of available scopes.

## Setting Environment Variables

Add the following lines to your `.env` file:

```
JIVE_CLIENT_ID=your_jive_client_id
JIVE_CLIENT_SECRET=your_jive_client_secret
```

## Usage Example

Once the environment variables are set, you can use the `JiveSSO` class to perform operations such as obtaining user info and sending emails.

```python
import os
from sso.jive import JiveSSO 

# Initialize the JiveSSO instance with the authorization code
jive_sso = JiveSSO(access_token='your_access_token', refresh_token='your_refresh_token')

# Fetch user info
user_info = jive_sso.get_user_info()
print(user_info)

# Send an email
response = jive_sso.send_email(to='recipient@example.com', subject='Test Email', message_text='This is a test email.')
print(response)
```

## Error Handling

The `JiveSSO` class is designed to handle authentication errors, such as token expiration. If the access token expires, it will automatically use the `refresh_token` to get a new access token.

## Conclusion

Setting up Jive SSO requires creating an OAuth application in your Jive instance, obtaining the `Client ID` and `Client Secret`, and setting the required scopes. By following the steps outlined in this document, you can integrate Jive SSO into your application and perform various actions such as fetching user information and sending emails.