from components.Auth import sso_redirect


def scopes():
    return [
        "pixiv.scope.profile.read",
    ]


def auth_uri():
    return "https://oauth.secure.pixiv.net/auth/authorize"


sso_redirect(provider="pixiv")
