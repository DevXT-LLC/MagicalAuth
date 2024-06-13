from components.Auth import sso_redirect


def scopes():
    return [
        "openid",
        "email",
    ]


def auth_uri():
    return "https://oauth.battle.net/authorize"


sso_redirect(provider="battlenet")
