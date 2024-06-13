from components.Auth import sso_redirect


def scopes():
    return [
        "basic",
        "email",
    ]


def auth_uri():
    return "https://secure.viadeo.com/oauth-provider/authorize"


sso_redirect(provider="viadeo")
