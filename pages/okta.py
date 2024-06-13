from components.Auth import sso_redirect


def scopes():
    return [
        "openid",
        "profile",
        "email",
    ]


def auth_uri():
    return "https://your-okta-domain/oauth2/v1/authorize"


sso_redirect(provider="okta")
