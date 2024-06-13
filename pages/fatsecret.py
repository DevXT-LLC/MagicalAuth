from components.Auth import sso_redirect


def scopes():
    return [
        "profile.get",  # Add the required scopes for FatSecret as appropriate
    ]


def auth_uri():
    return "https://oauth.fatsecret.com/connect/authorize"


sso_redirect(provider="fatsecret")
