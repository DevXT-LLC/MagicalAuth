from components.Auth import sso_redirect


def scopes():
    return [
        "read",
        "activity:write",
    ]


def auth_uri():
    return "https://www.strava.com/oauth/authorize"


sso_redirect(provider="strava")
