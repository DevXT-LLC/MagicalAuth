from components.Auth import sso_redirect


def scopes():
    return ["read", "write"]


def auth_uri():
    return "https://<your-zendesk-subdomain>.zendesk.com/oauth/authorizations/new"


sso_redirect(provider="zendesk")
