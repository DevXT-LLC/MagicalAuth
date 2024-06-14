## NetIQ

### Required Environment Variables

To integrate NetIQ single sign-on (SSO) in your application, you need to set the following environment variables:

- `NETIQ_CLIENT_ID`: NetIQ OAuth client ID
- `NETIQ_CLIENT_SECRET`: NetIQ OAuth client secret

### Steps to Acquire NetIQ Client ID and Client Secret

1. **Log in to your NetIQ Admin Console**:
   - Access the NetIQ admin console through your provided administrative URL.
   
2. **Register a New OAUTH Application**:
   - Navigate to the `OAuth` section within the admin console.
   - Add a new application by providing all the necessary details such as application name, redirect URIs, etc.

3. **Obtain `Client ID` and `Client Secret`**:
   - After successfully registering your application, NetIQ will provide you with a `Client ID` and `Client Secret`.

4. **Set Environment Variables**:
   - Add `NETIQ_CLIENT_ID` and `NETIQ_CLIENT_SECRET` to your .env file:
     ```dotenv
     NETIQ_CLIENT_ID=your-netiq-client-id
     NETIQ_CLIENT_SECRET=your-netiq-client-secret
     ```

### Required APIs

Ensure that the required APIs are enabled in your NetIQ settings. Usually, this can be found in the API Management section of the admin console.

### Required Scopes for NetIQ OAuth

Make sure to include the following scopes for your NetIQ OAuth authorization:

- `profile`
- `email`
- `openid`
- `user.info`

### Example Code to Utilize NetIQ SSO

The provided `NetIQSSO` class can be used to manage the complete OAuth flow, fetch user information, and send emails using the NetIQ API. Here’s a quick example of how to leverage this class:

#### Integrating NetIQSSO

```python
from sso.netiq import NetIQSSO, netiq_sso

# Initialize with the authorization code
code = "your-authorization-code"
redirect_uri = "http://your-redirect-url"
netiq_instance = netiq_sso(code, redirect_uri)

if netiq_instance:
    # Fetch user information
    user_info = netiq_instance.user_info
    print(f"User Email: {user_info['email']}")
    print(f"User First Name: {user_info['first_name']}")
    print(f"User Last Name: {user_info['last_name']}")

    # Send an email using NetIQ
    response = netiq_instance.send_email("recipient@example.com", "Subject", "Message Text")
    print("Email Send Response:", response)
else:
    print("Failed to initialize NetIQSSO instance")
```

### netiq_sso Function

The `netiq_sso` function is a helper function that makes the OAuth authorization code flow easy to handle. It exchanges an authorization code for an access token and initializes the `NetIQSSO` instance.

#### Usage

1. Obtain the authorization code as part of your OAuth flow.
2. Call the `netiq_sso` function with the code and your redirect URI.

### Error Handling

The `NetIQSSO` class has built-in error handling to manage token expiration and refresh scenarios. If an access token is expired, it will automatically refresh it using the refresh token.

By following these steps, you should be able to quickly and easily set up your environment for working with NetIQ SSO in your application.