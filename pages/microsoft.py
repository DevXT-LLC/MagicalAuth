from components.Auth import sso_redirect


def scopes():
    return [
        "https://graph.microsoft.com/User.Read https://graph.microsoft.com/Mail.Send",
        "https://graph.microsoft.com/Calendars.ReadWrite.Shared",
    ]


def auth_uri():
    return "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"


sso_redirect(provider="microsoft")
