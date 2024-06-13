from components.Auth import sso_redirect


def scopes():
    return [
        "bitly:read",
        "bitly:write",
    ]


def auth_uri():
    return "https://bitly.com/oauth/authorize"


sso_redirect(provider="bitly")
