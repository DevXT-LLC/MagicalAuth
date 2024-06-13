from components.Auth import sso_redirect


def scopes():
    return [
        "account",
        "email",
    ]


def auth_uri():
    return "https://bitbucket.org/site/oauth2/authorize"


sso_redirect(provider="bitbucket")
