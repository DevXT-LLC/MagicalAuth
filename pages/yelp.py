from components.Auth import sso_redirect


def scopes():
    return [
        "business",
    ]


def auth_uri():
    return "https://api.yelp.com/oauth2/authorize"


sso_redirect(provider="yelp")
