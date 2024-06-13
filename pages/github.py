from components.Auth import sso_redirect


def scopes():
    return ["user:email", "read:user"]


def auth_uri():
    return "https://github.com/login/oauth/authorize"


sso_redirect(provider="github")
