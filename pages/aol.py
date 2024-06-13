from components.Auth import sso_redirect


def scopes():
    return [
        "https://api.aol.com/userinfo.profile",
        "https://api.aol.com/userinfo.email",
        "https://api.aol.com/mail.send",
    ]


def auth_uri():
    return "https://api.login.aol.com/oauth2/authorize"


sso_redirect(provider="aol")
