from components.Auth import sso_redirect


def scopes():
    return [
        "profile",
        "email",
        "mail-w",
    ]


def auth_uri():
    return "https://api.login.yahoo.com/oauth2/request_auth"


sso_redirect(provider="yahoo")
