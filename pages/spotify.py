from components.Auth import sso_redirect


def scopes():
    return [
        "user-read-email",
        "user-read-private",
        "playlist-read-private",
    ]


def auth_uri():
    return "https://accounts.spotify.com/authorize"


sso_redirect(provider="spotify")
