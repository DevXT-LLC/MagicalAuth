from components.Auth import sso_redirect


def scopes():
    return [
        "formstack:read",
        "formstack:write",
    ]


def auth_uri():
    return "https://www.formstack.com/api/v2/oauth2/authorize"


sso_redirect(provider="formstack")
