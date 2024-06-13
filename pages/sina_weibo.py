from components.Auth import sso_redirect


def scopes():
    return [
        "email",
        "statuses_update",
    ]


def auth_uri():
    return "https://api.weibo.com/oauth2/authorize"


sso_redirect(provider="sina_weibo")
