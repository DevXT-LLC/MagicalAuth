from components.Auth import sso_redirect


def scopes():
    return [
        "/authenticate",
        "/activities/update",
    ]


def auth_uri():
    return "https://orcid.org/oauth/authorize"


sso_redirect(provider="orcid")
