from components.Auth import sso_redirect


def scopes():
    return [
        "user.info.read",
        "email.send",
    ]


def auth_uri():
    return "https://auth.clearscore.com/oauth2/authorize"


sso_redirect(provider="clearscore")
