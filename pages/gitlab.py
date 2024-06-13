from components.Auth import sso_redirect


def scopes():
    return [
        "read_user",
        "api",
        "email",
    ]


def auth_uri():
    return "https://gitlab.com/oauth/authorize"


sso_redirect(provider="gitlab")
