from components.Auth import sso_redirect


def scopes():
    return [
        "email",
        # Add other necessary scopes if needed
    ]


def auth_uri():
    return "https://oauth.vk.com/authorize"


sso_redirect(provider="vk")
