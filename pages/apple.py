from components.Auth import sso_redirect


def scopes():
    return [
        "name",
        "email",
    ]


def auth_uri():
    return "https://appleid.apple.com/auth/authorize"


sso_redirect(provider="apple")
