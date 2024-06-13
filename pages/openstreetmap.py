from components.Auth import sso_redirect


def scopes():
    return ["read_prefs"]


def auth_uri():
    return "https://www.openstreetmap.org/oauth/authorize"


sso_redirect(provider="openstreetmap")
