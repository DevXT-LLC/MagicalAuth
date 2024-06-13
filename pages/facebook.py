from components.Auth import sso_redirect


def scopes():
    return [
        "public_profile",
        "email",
        "pages_messaging",
    ]


def auth_uri():
    return "https://www.facebook.com/v10.0/dialog/oauth"


sso_redirect(provider="facebook")
