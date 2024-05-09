# MagicalAuth

MagicalAuth is a simple but magical authentication system for Python applications. It is designed to be easy to use and easy to understand. It is also designed to be secure and reliable utilizing magic links and multi-factor authentication.

## Environment Variables

- `ENCRYPTION_SECRET`: The secret key used to encrypt and decrypt the magic link tokens. This should be a long random string.
- `MAGIC_LINK_URL`: The URL that the magic link will point to. This should be the URL of the application that will handle the magic link. It will send query parameters `email` and `token` to this URL that will be used on the `/login` endpoint to authenticate the user.
- `SENDGRID_API_KEY`: The API key for SendGrid. This is used to send the magic link email to the user.
- `SENDGRID_FROM_EMAIL`: The email address that the magic link email will be sent from. This should be a verified email address in SendGrid.
- `REGISTRATION_WEBHOOK`: The URL that the registration webhook will be sent to. This should be the URL of the application that will handle the registration webhook. It will send a POST request with a JSON body containing the user's email address.

## Usage

```bash
docker-compose down && docker-compose pull && docker-compose up
```

Access the FastAPI documentation at `http://localhost:14374` .

## UI Example

See [UI.py](UI.py) for an example of how to use MagicalAuth in a Streamlit application. You can run it with the following command:

```bash
streamlit run UI.py
```
