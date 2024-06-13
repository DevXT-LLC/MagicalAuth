from components.Auth import sso_redirect


def scopes():
    return [
        "profile",
        "email",
        "openid",
    ]


def auth_uri():
    return "https://auth.pingidentity.com/as/authorize.oauth2"


sso_redirect(provider="ping_identity")
