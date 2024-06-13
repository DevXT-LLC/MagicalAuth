from components.Auth import sso_redirect


def scopes():
    return ["user:read:email"]


def auth_uri():
    return "https://id.twitch.tv/oauth2/authorize"


sso_redirect(provider="twitch")
