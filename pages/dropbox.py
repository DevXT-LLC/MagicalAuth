from components.Auth import sso_redirect


def scopes():
    return [
        "account_info.read",
        "files.metadata.read",
    ]


def auth_uri():
    return "https://www.dropbox.com/oauth2/authorize"


sso_redirect(provider="dropbox")
