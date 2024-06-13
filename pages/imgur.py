from components.Auth import sso_redirect


def scopes():
    return [
        "read",
        "write",
    ]


def auth_uri():
    return "https://api.imgur.com/oauth2/authorize"


sso_redirect(provider="imgur")
