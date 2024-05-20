# MagicalAuth

MagicalAuth is a simple but magical authentication system for Python applications. It is designed to be easy to use and easy to understand. It is also designed to be secure and reliable utilizing magic links and multi-factor authentication.

## Environment Variables

- `APP_NAME`: The name of the application. This will be used in the magic link email to the user.
- `ALLOWED_DOMAINS`: A comma-separated list of allowed email domains. If this is set, only users with email addresses from these domains will be allowed to register and login. If this is not set, it will default to `*` and all email domains will be allowed.
- `ENCRYPTION_SECRET`: The secret key used to encrypt and decrypt the magic link tokens. This should be a long random string.
- `MAGICALAUTH_SERVER`: The URL of the MagicalAuth server. This should be the URL of the server that is running the MagicalAuth FastAPI service.
- `MAGIC_LINK_URL`: The URL that the magic link will point to. This should be the URL of the application that will handle the magic link. It will send query parameters `email` and `token` to this URL that will be used on the `MAGIC_LINK_URL` endpoint to authenticate the user.
- `SENDGRID_API_KEY`: The API key for SendGrid. This is used to send the magic link email to the user.
- `SENDGRID_FROM_EMAIL`: The email address that the magic link email will be sent from. This should be a verified email address in SendGrid.
- `REGISTRATION_WEBHOOK`: The URL that the registration webhook will be sent to. This should be the URL of the application that will handle the registration webhook. It will send a POST request with a JSON body containing the user's email address.
- `DATABASE_USER`: The username for the PostgreSQL database.
- `DATABASE_PASSWORD`: The password for the PostgreSQL database.
- `DATABASE_HOST`: The host for the PostgreSQL database.
- `DATABASE_PORT`: The port for the PostgreSQL database.
- `DATABASE_NAME`: The name of the PostgreSQL database.
- `LOGLEVEL`: The log level for the application. This should be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.

## Usage

```bash
docker-compose down && docker-compose pull && docker-compose up
```

Access the FastAPI documentation at `http://localhost:12437` .

### Web User Interface

See [UI.py](UI.py) for an example of how to use MagicalAuth in a Streamlit application. It runs with the FastAPI service in the Docker Compose setup.

Access the Streamlit UI at `http://localhost:8519` .
