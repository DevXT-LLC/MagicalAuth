from components.Auth import sso_redirect


def scopes():
    return [
        "https://api.xing.com/v1/users/me",
        "https://api.xing.com/v1/authorize",
    ]


def auth_uri():
    return "https://api.xing.com/v1/authorize"


sso_redirect(provider="xing")
