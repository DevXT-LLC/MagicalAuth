from components.Auth import sso_redirect


def scopes():
    return ["refresh_token full email"]


def auth_uri():
    return "https://login.salesforce.com/services/oauth2/authorize"


sso_redirect(provider="salesforce")
