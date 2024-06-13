from components.Auth import sso_redirect


def scopes():
    return [
        "user_profile",
        "user_media",
    ]


def auth_uri():
    return "https://api.instagram.com/oauth/authorize"


sso_redirect(provider="instagram")
