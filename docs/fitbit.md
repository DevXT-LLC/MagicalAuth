## Fitbit

### Required environment variables

- `FITBIT_CLIENT_ID`: Fitbit OAuth client ID
- `FITBIT_CLIENT_SECRET`: Fitbit OAuth client secret

### Required APIs

Before using the Fitbit SSO, you need to confirm that you have the necessary APIs enabled and have acquired the required environment variables (FITBIT_CLIENT_ID, FITBIT_CLIENT_SECRET). Follow the steps below to do this:

1. **Create a Fitbit Developer Account**:
   - Go to the Fitbit dev portal: [Fitbit Developer](https://dev.fitbit.com/)
   - Create an account or log in if you already have one.

2. **Register Your Application**:
   - Navigate to the "Manage my Apps" section.
   - Click on "Register a New Application".
   - Fill out the application details. 
   - Set the OAuth 2.0 Application Type to "Personal" or "Server".

3. **Obtain Client ID and Client Secret**:
   - After registering your application, Fitbit will provide you with a **Client ID** and **Client Secret**.

4. **Set Up Environment Variables**:
   - Create or update your `.env` file with the following:
     ```
     FITBIT_CLIENT_ID=your_fitbit_client_id
     FITBIT_CLIENT_SECRET=your_fitbit_client_secret
     ```

### Required Scopes for Fitbit OAuth

When configuring OAuth for Fitbit, you need to request the appropriate permissions (scopes). Below are the required scopes:

- `activity`
- `heartrate`
- `location`
- `nutrition`
- `profile`
- `settings`
- `sleep`
- `social`
- `weight`

To set these scopes when registering your Fitbit application or generating an access token, you will typically provide them as a space-separated string.

Example: 
```
activity heartrate location nutrition profile settings sleep social weight
```

### Example Usage

Here’s an example of how to use the `fitbit_sso` function to integrate Fitbit SSO in your application:

```python
from fitbit import fitbit_sso

# After getting authorization code from Fitbit via the OAuth flow
authorization_code = "your_authorization_code"
redirect_uri = "your_redirect_uri"  # Optional, fallback to MAGIC_LINK_URL in env if not supplied.

fitbit_instance, error = fitbit_sso(authorization_code, redirect_uri)

if error:
    print("SSO Error:", error)
else:
    print("Access Token:", fitbit_instance.access_token)
    print("User Info:", fitbit_instance.user_info)

    # Fetch activities
    activities = fitbit_instance.get_activities()
    print("User Activities:", activities)
```

### Error Handling

During the OAuth operations, if there's an issue (e.g., invalid credentials, expired tokens), appropriate HTTP exceptions are raised with relevant details. The logging module captures detailed error messages which can be useful for debugging:

- **Get New Token Error**:
  If refreshing the access token fails, an `HTTPException` with status code `403` is raised, and an error message is logged.
  
- **Fetch User Info Error**:
  If fetching user info from Fitbit fails, an `HTTPException` with status code `400` is raised, and an error message is logged.
  
- **Fetch Activities Error**:
  If fetching user activities fails, the error details are logged and an `HTTPException` with the relevant status code is raised.

By ensuring that the required environment variables and keys are correctly configured, and handling potential errors gracefully, you can integrate Fitbit's rich suite of APIs into your application seamlessly.