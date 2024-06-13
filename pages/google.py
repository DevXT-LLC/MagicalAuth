from components.Auth import sso_redirect


def scopes():
    return [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ]


def auth_uri():
    return "https://accounts.google.com/o/oauth2/auth"


sso_redirect(provider="google")
