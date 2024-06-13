from components.Auth import sso_redirect


def scopes():
    return [
        "activity",
        "heartrate",
        "location",
        "nutrition",
        "profile",
        "settings",
        "sleep",
        "social",
        "weight",
    ]


def auth_uri():
    return "https://www.fitbit.com/oauth2/authorize"


sso_redirect(provider="fitbit")
