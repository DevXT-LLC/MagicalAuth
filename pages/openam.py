from components.Auth import sso_redirect


def scopes():
    return [
        "profile",
        "email",
    ]


def auth_uri():
    return "https://your-openam-base-url/oauth2/authorize"


sso_redirect(provider="openam")
