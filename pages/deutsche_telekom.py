from components.Auth import sso_redirect


def scopes():
    return [
        "t-online-profile",
        "t-online-email",
    ]


def auth_uri():
    return "https://www.telekom.com/ssoservice/authorize"


sso_redirect(provider="deutsche_telekom")
