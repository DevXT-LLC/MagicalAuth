from components.Auth import sso_redirect


def scopes():
    return [
        "messages:email",
        "messages:post",
    ]


def auth_uri():
    return "https://www.yammer.com/oauth2/authorize"


sso_redirect(provider="yammer")
