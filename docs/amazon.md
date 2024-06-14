# Amazon SSO

## Overview

This module provides Single Sign-On (SSO) functionality using AWS Cognito, allowing users to authenticate and fetch user information. Additionally, it includes the functionality to send emails using Amazon SES (Simple Email Service).

## Required Environment Variables

To use the Amazon SSO module, you need to set up the following environment variables. These credentials can be acquired from the AWS Management Console.

```plaintext
AWS_CLIENT_ID: AWS Cognito OAuth client ID
AWS_CLIENT_SECRET: AWS Cognito OAuth client secret
AWS_USER_POOL_ID: AWS Cognito User Pool ID
AWS_REGION: AWS Cognito Region
MAGIC_LINK_URL: A redirect URI to be used after the SSO login (optional)
```

### Step-by-Step Guide to Acquire the Required Keys

1. **AWS Client ID and Client Secret**:
    - Navigate to the [Amazon Cognito Console](https://console.aws.amazon.com/cognito/home).
    - Click on **Manage User Pools** and select the user pool you have set up for your application.
    - Navigate to the **App integration** section.
    - Under **App clients and analytics**, find your app client or create one by clicking **Add an app client**.
    - Save the **App client id** and **App client secret** as they will be your `AWS_CLIENT_ID` and `AWS_CLIENT_SECRET`.

2. **AWS User Pool ID**:
    - In the Cognito User Pool you've set up, the **User Pool ID** is displayed at the top of the **General settings** section in the details page of your user pool. Assign this value to `AWS_USER_POOL_ID`.

3. **AWS Region**:
    - The region in which your Cognito User Pool is located, such as `us-west-2`. Assign this value to `AWS_REGION`.

4. **Magic Link URL**:
    - This is a redirect URI used after the SSO login process. It's typically the URL where your application handles the redirect after authentication. Assign this value to `MAGIC_LINK_URL`. This is optional and can be set to any valid URL your application accepts for OAuth callbacks.

## Required Scopes for AWS OAuth

Include the following scopes in your OAuth configuration to get relevant user information and send emails:
- openid
- email
- profile

## Using the AmazonSSO Class

### Initialization

Initialize the `AmazonSSO` class with the access and refresh tokens:

```python
sso = AmazonSSO(access_token='your-access-token', refresh_token='your-refresh-token')
```

### Fetching User Info

You can fetch the user info by accessing the `user_info` attribute:

```python
user_info = sso.user_info
print(user_info)
```

### Sending an Email

To send an email using Amazon SES, use the `send_email` method:

```python
response = sso.send_email(
    to="recipient@example.com",
    subject="Your Subject",
    message_text="Your message body."
)
print(response)
```

## Example Code

Below is an example of how to use the AmazonSSO class in your application:

```python
from sso.amazon import AmazonSSO, amazon_sso

# Example: Fetching user info using authorization code

code = "authorization-code"
sso_instance, error = amazon_sso(code)

if sso_instance:
    user_info = sso_instance.user_info
    print(user_info)
else:
    print("Error during SSO:", error)

# Example: Sending an email

sso_instance.send_email(
    to="recipient@example.com",
    subject="Greetings",
    message_text="Hello from AWS SSO!"
)
```

With these steps and examples, you should be able to set up and utilize AWS Cognito-based SSO and Amazon SES for email sending. Ensure you have the appropriate permissions and configurations set in your AWS account to use these features effectively.