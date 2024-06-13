from components.Auth import sso_redirect


def scopes():
    return ["cloud_controller.read", "openid", "email"]


def auth_uri():
    return "https://login.system.example.com/oauth/authorize"  # Replace with the actual authorization URL


sso_redirect(provider="cloud_foundry")
