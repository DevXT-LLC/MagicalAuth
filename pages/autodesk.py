from components.Auth import sso_redirect


def scopes():
    return [
        "data:read",
        "data:write",
        "bucket:read",
        "bucket:create",
    ]


def auth_uri():
    return "https://developer.api.autodesk.com/authentication/v1/authorize"


sso_redirect(provider="autodesk")
