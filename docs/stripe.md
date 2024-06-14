## Stripe

### Required Environment Variables

To use Stripe SSO, ensure that the following environment variables are set:

- `STRIPE_CLIENT_ID`: Your Stripe OAuth client ID.
- `STRIPE_CLIENT_SECRET`: Your Stripe OAuth client secret.

### Required Scopes for Stripe SSO

Make sure you have the required scope for Stripe SSO:

- `read_write`

### How to Acquire Required Keys

1. **Create a Stripe Account**: If you don't have a Stripe account, sign up at [Stripe](https://stripe.com/).
2. **Create a New Project**: Once logged in, navigate to your dashboard and create a new project.
3. **Get Your Client ID and Secret**: Go to "Developers" > "API keys". Here you will find your client ID and secret:
   - **Client ID**: This is your OAuth client ID used for authentication.
   - **Client Secret**: This is your OAuth client secret that should be kept secure.

### Setting Up Environment Variables

Once you have your client ID and secret, add them to your environment variables. If you’re using a `.env` file, it should look like this:

```env
STRIPE_CLIENT_ID=your_stripe_client_id
STRIPE_CLIENT_SECRET=your_stripe_client_secret
```

### Example Usage

Here’s how to use the provided `StripeSSO` class in your application:

1. **Import the `StripeSSO` class**:
    ```python
    from sso.stripe import StripeSSO, stripe_sso
    ```

2. **Authenticate using the `stripe_sso` function**: This function takes an authorization code and an optional redirect URI.
    ```python
    code = "your_authorization_code"
    redirect_uri = "your_redirect_uri"  # Optional, if not provided, defaults to MAGIC_LINK_URL environment variable

    stripe_sso_instance = stripe_sso(code, redirect_uri)
    ```

3. **Access User Information**: Once authenticated, you can access user information through the `stripe_sso_instance`.
    ```python
    user_info = stripe_sso_instance.user_info
    print(user_info["email"])
    print(user_info["business_name"])
    ```

### Notes

- **Refreshing Tokens**: The `StripeSSO` class handles refreshing tokens for you. If an access token expires, it will automatically use the refresh token to get a new one.
- **Error Handling**: If there is a problem retrieving user information from Stripe, an HTTPException will be raised with a status code of 400.

By following these steps, you can quickly and easily set up your Stripe SSO integration.