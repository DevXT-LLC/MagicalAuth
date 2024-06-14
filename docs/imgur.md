# Imgur SSO Integration Documentation

This documentation provides details on setting up and using the Imgur Single Sign-On (SSO) integration. The Imgur SSO integration allows users to authenticate and interact with Imgur's API for actions like uploading images and retrieving user information.

## Required Environment Variables

To use the Imgur SSO functionality, you'll need to set the following environment variables:

- `IMGUR_CLIENT_ID`: Imgur OAuth client ID
- `IMGUR_CLIENT_SECRET`: Imgur OAuth client secret

## Steps to Acquire Required Keys

1. **Create an Imgur Application:**
   - Go to the [Imgur API Applications page](https://api.imgur.com/oauth2/addclient).
   - Log in with your Imgur account.
   - Fill out the required fields to register a new application. You'll need to provide:
     - **Application Name**: Choose a name for your application.
     - **Authorization Type**: Select `OAuth 2 authorization with a callback URL`.
     - **Authorization callback URL**: Enter the URL where you want users to be redirected after authorization (e.g., `http://localhost:3000/callback`).
   - After submitting the form, you will receive the `Client ID` and `Client Secret`. These values are required for environment variables.

2. **Set Environment Variables:**
   - Add the obtained `Client ID` and `Client Secret` to your environment configuration file (e.g., `.env` file).

     ```plaintext
     IMGUR_CLIENT_ID=your_imgur_client_id
     IMGUR_CLIENT_SECRET=your_imgur_client_secret
     ```

## Required Scopes for Imgur SSO

To enable the required functionalities, ensure that your application requests the following scopes when users authenticate:

- `read`: Allows reading user data and images.
- `write`: Allows uploading images and other write operations.

## Example Usage

Here's a detailed breakdown of how to use the Imgur SSO integration:

1. **Initialize ImgurSSO:**
   - Create an instance of the `ImgurSSO` class with access and refresh tokens.

     ```python
     from imgur import ImgurSSO

     access_token = "your_access_token"
     refresh_token = "your_refresh_token"
     imgur_sso = ImgurSSO(access_token=access_token, refresh_token=refresh_token)
     ```

2. **Get User Information:**
   - Retrieve the authenticated user's information such as username and email.

     ```python
     user_info = imgur_sso.get_user_info()
     print(user_info)  # Output: {'username': 'your_username', 'email': 'your_email'}
     ```

3. **Upload an Image:**
   - Upload an image to Imgur by providing the image file path and optional title and description.

     ```python
     image_path = "path/to/your/image.jpg"
     title = "Image Title"
     description = "Image Description"
     upload_response = imgur_sso.upload_image(image_path, title, description)
     print(upload_response)
     ```

4. **Handle Authorization and Token Refresh:**
   - If the access token expires, the `ImgurSSO` class will handle refreshing the token automatically and retrying the request.

5. **Imgur SSO Authentication:**
   - Use the `imgur_sso` function to authenticate using an authorization code obtained via the OAuth flow.

     ```python
     from imgur import imgur_sso

     authorization_code = "your_authorization_code"
     redirect_uri = "http://localhost:3000/callback"
     sso_instance = imgur_sso(authorization_code, redirect_uri=redirect_uri)
     ```

6. **Handle Possible Errors:**
   - The module uses FastAPI's `HTTPException` to handle errors. Ensure you handle possible exceptions in your application.

     ```python
     try:
         user_info = imgur_sso.get_user_info()
     except HTTPException as e:
         print(f"Error: {e.detail}")
     ```

By following these steps, you can integrate and use Imgur's SSO functionality in your application. Ensure you have the necessary environment variables properly set up and that your OAuth flow is correctly configured to handle user authentication and token management.