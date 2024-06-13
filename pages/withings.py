from components.Auth import sso_redirect


def scopes():
    return [
        "user.info",
        "user.metrics",
        "user.activity",
    ]


def auth_uri():
    return "https://account.withings.com/oauth2_user/authorize2"


sso_redirect(provider="withings")
