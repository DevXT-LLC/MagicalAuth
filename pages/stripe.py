from components.Auth import sso_redirect


def scopes():
    return [
        "read_write",
    ]


def auth_uri():
    return "https://connect.stripe.com/oauth/authorize"


sso_redirect(provider="stripe")
