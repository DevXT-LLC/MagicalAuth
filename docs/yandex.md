## Yandex

### Required Environment Variables

To integrate Yandex SSO into your application, you need to set the following environment variables:

- `YANDEX_CLIENT_ID`: Your Yandex OAuth client ID.
- `YANDEX_CLIENT_SECRET`: Your Yandex OAuth client secret.

### Required APIs

Make sure the necessary APIs are enabled in your Yandex application.

### Required Scopes for Yandex OAuth

These OAuth scopes are required for Yandex SSO:

- `login:info`
- `login:email`
- `mail.send`

### Setting Up

#### Step 1: Register Your Application

1. Go to the [Yandex OAuth Application dashboard](https://oauth.yandex.com/client/new).
2. Click on the "Create an application" button.
3. Fill out the form with your application details.
4. Note down the `YANDEX_CLIENT_ID` and `YANDEX_CLIENT_SECRET` provided by Yandex.

#### Step 2: Enable Required Scopes

1. Navigate to the "Permissions" section of your application.
2. Add the following scopes:
   - `login:info`
   - `login:email`
   - `mail.send`

#### Step 3: Add Environment Variables

Add the `YANDEX_CLIENT_ID` and `YANDEX_CLIENT_SECRET` to your `.env` file:

```plaintext
YANDEX_CLIENT_ID=your_yandex_client_id
YANDEX_CLIENT_SECRET=your_yandex_client_secret
```

### Example Usage

This is how you can use the YandexSSO class in your application:

```python
from yandex import YandexSSO

# Assuming you have obtained an OAuth authorization code
code = "your_authorization_code"

# Instantiate the YandexSSO class
yandex_sso_instance = yandex_sso(code)

# Get user info
user_info = yandex_sso_instance.user_info
print(user_info)

# Send an email using Yandex's SMTP service
to_email = "recipient@example.com"
subject = "Your email subject"
message_text = "Your email message"
yandex_sso_instance.send_email(to_email, subject, message_text)
```

By following these steps, you can successfully set up Yandex SSO in your application. Ensure that you have added the required environment variables and enabled the correct scopes to avoid any issues.