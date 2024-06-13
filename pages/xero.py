from components.Auth import sso_redirect


def scopes():
    return ["openid", "profile", "email", "offline_access"]


def auth_uri():
    return "https://login.xero.com/identity/connect/authorize"


sso_redirect(provider="xero")
