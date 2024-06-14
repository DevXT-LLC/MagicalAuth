## Intel Cloud Services

The `intel_cloud_services.py` script allows for the integration with Intel's OAuth services for Single Sign-On (SSO) and email sending capabilities through their API.

### Required Environment Variables

To use the Intel Cloud Services, you need to set up the following environment variables:

- `INTEL_CLIENT_ID`: Intel OAuth client ID
- `INTEL_CLIENT_SECRET`: Intel OAuth client secret

### How to Obtain the Required Environment Variables

#### Step 1: Create an Intel Developer Account

1. Go to the [Intel Developer Zone](https://developer.intel.com).
2. Register for an account if you don't have one.
3. Log in to your Intel Developer account.

#### Step 2: Create an Application

1. Navigate to the [Intel APIs](https://developer.intel.com/apis).
2. Create a new application and obtain its Client ID and Client Secret.
   - **Client ID**: This will be your `INTEL_CLIENT_ID`.
   - **Client Secret**: This will be your `INTEL_CLIENT_SECRET`.

#### Step 3: Enable Required APIs

Make sure the following APIs are enabled for your application:
- User Info API
- Mail Send API

### Required Scopes for Intel SSO

The following scopes must be added to your OAuth application settings:

- `https://api.intel.com/userinfo.read`
- `https://api.intel.com/mail.send`

### Setting Up Your .env File

Add the acquired `INTEL_CLIENT_ID` and `INTEL_CLIENT_SECRET` to your `.env` file:

```plaintext
INTEL_CLIENT_ID=your_client_id_here
INTEL_CLIENT_SECRET=your_client_secret_here
```

### Example Usage

Here's how you can use the IntelSSO class in your project:

#### Initialize IntelSSO with Authorization Code

```python
from sso.intel_cloud_services import intel_cloud_services_sso

# Assume `code` is obtained from the OAuth callback
intel_sso_instance = intel_cloud_services_sso(code)

if intel_sso_instance:
    # Get user info
    user_info = intel_sso_instance.get_user_info()
    print("User Info:", user_info)

    # Send an email
    response = intel_sso_instance.send_email(
        to="recipient@example.com",
        subject="Test Email",
        message_text="Hello from IntelSSO"
    )
    print("Email Response:", response)
else:
    print("Failed to initialize IntelSSO")
```

### Class Documentation

#### Class: `IntelSSO`

##### Constructor: `__init__(self, access_token=None, refresh_token=None)`

- **Parameters:**
  - `access_token`: Access token for Intel API.
  - `refresh_token`: Refresh token for Intel API.

##### Method: `get_new_token(self)`

- **Returns:** str
- **Description:** Returns a new access token using the refresh token.

##### Method: `get_user_info(self)`

- **Returns:** dict
- **Description:** Retrieves the user's information (email, first name, last name) using the access token.

##### Method: `send_email(self, to, subject, message_text)`

- **Parameters:**
  - `to`: Recipient email address.
  - `subject`: Subject of the email.
  - `message_text`: Text content of the email.
- **Returns:** dict
- **Description:** Sends an email using the Intel API.

By following these steps, you will be able to set up your environment and use the Intel Cloud Services for authentication and email sending functionalities.