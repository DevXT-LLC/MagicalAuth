from components.Auth import sso_redirect


def scopes():
    return [
        "identify",
        "email",
    ]


def auth_uri():
    return "https://discord.com/api/oauth2/authorize"


sso_redirect(provider="discord")
