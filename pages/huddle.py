from components.Auth import sso_redirect


def scopes():
    return [
        "user_info",
        "send_email",
    ]


def auth_uri():
    return "https://login.huddle.com/oauth2/authorize"


sso_redirect(provider="huddle")
