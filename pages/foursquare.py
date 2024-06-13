from components.Auth import sso_redirect


def scopes():
    # Foursquare does not require specific scopes for basic user info.
    return []


def auth_uri():
    return "https://foursquare.com/oauth2/authenticate"


sso_redirect(provider="foursquare")
