from components.Auth import sso_redirect


def scopes():
    return [
        "user",
        "browse",
        "stash",
        "send_message",
    ]


def auth_uri():
    return "https://www.deviantart.com/oauth2/authorize"


sso_redirect(provider="deviantart")
