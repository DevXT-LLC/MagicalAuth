from components.Auth import sso_redirect
from Globals import getenv


def scopes():
    return [
        "openid",
        "email",
        "profile",
    ]


def auth_uri():
    return f"https://{getenv('AWS_USER_POOL_ID')}.auth.{getenv('AWS_REGION')}.amazoncognito.com/oauth2/authorize"


sso_redirect(provider="amazon")
