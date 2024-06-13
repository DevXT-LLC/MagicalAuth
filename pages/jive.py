from components.Auth import sso_redirect


def scopes():
    return ["your_required_scopes_here"]


def auth_uri():
    return "https://example.jive.com/oauth2/authorize"


sso_redirect(provider="jive")
