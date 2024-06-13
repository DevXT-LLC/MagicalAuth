from components.Auth import sso_redirect


def scopes():
    return [
        "openid",
        "email",
        "profile",
    ]


def auth_uri():
    return "https://your-keycloak-server/auth/realms/your-realm/protocol/openid-connect/auth"


sso_redirect(provider="keycloak")
