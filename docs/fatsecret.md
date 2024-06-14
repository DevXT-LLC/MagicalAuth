## FatSecret

## Required environment variables

- `FATSECRET_CLIENT_ID`: FatSecret OAuth client ID
- `FATSECRET_CLIENT_SECRET`: FatSecret OAuth client secret

Ensure that these environment variables are added to your `.env` file.

## Required APIs

To use FatSecret's services, you need to register your application and obtain client credentials by following these steps:

1. Go to the [FatSecret Platform](https://platform.fatsecret.com/api/).
2. Click on "Sign Up" to create an account or log in if you already have one.
3. Once logged in, create a new application to get your `client_id` and `client_secret`.

## Setting up your environment variables

After acquiring your `FATSECRET_CLIENT_ID` and `FATSECRET_CLIENT_SECRET`, add them to your `.env` file like this:

```plaintext
FATSECRET_CLIENT_ID=your_fatsecret_client_id
FATSECRET_CLIENT_SECRET=your_fatsecret_client_secret
MAGIC_LINK_URL=your_redirect_uri
```

Ensure that your `.env` file is in the root directory of your project, and that the `getenv` function in your code can access these environment variables.

## Example Usage

Here is a basic example of how to use the `FatSecretSSO` class and the `fatsecret_sso` function:

1. **Initialize FatSecretSSO with an authorization code:**

    ```python
    from sso.fatsecret import fatsecret_sso

    # This code is usually obtained as part of the OAuth redirection process
    authorization_code = "your_authorization_code"
    redirect_uri = "your_redirect_uri" # Same as the REDIRECT_URL in your .env file

    fatsecret_instance = fatsecret_sso(authorization_code, redirect_uri)
    if fatsecret_instance is None:
        print("Error initializing FatSecret SSO")
    else:
        print("FatSecret SSO initialized successfully")
        user_info = fatsecret_instance.user_info
        print(f"User Info: {user_info}")
    ```

2. **Refresh Access Token Example:**

    If your access token expires, you can refresh it using the `get_new_token` method:

    ```python
    refresh_token = "your_refresh_token"
    
    # Initialize with existing tokens
    fatsecret_instance = FatSecretSSO(access_token="existing_access_token", refresh_token=refresh_token)
    
    new_access_token = fatsecret_instance.get_new_token()
    print(f"New Access Token: {new_access_token}")
    ```

3. **Get User Information:**

    Once you have an `access_token`, you can get user information using the `get_user_info` method:

    ```python
    user_info = fatsecret_instance.get_user_info()
    print(f"User Info: {user_info}")
    ```

This completes the basic setup and usage instructions for FatSecret SSO in your application. Ensure that the required APIs and credentials are correctly set up to avoid any issues during the authentication process.