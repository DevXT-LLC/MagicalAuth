from components.Auth import sso_redirect


def scopes():
    return [
        "profile",
        "email",
        "openid",
        "user.info",
    ]


def auth_uri():
    return "https://your-netiq-domain.com/oauth2/authorize"


sso_redirect(provider="netiq")
