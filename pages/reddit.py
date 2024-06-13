from components.Auth import sso_redirect


def scopes():
    return [
        "identity",
        "submit",
        "read",
    ]


def auth_uri():
    return "https://www.reddit.com/api/v1/authorize"


sso_redirect(provider="reddit")
