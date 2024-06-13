from components.Auth import sso_redirect


def scopes():
    return [
        "https://launchpad.37signals.com/authorization/new",
        "https://3.basecampapi.com/{account_id}/people/me.json",
    ]


def auth_uri():
    return "https://launchpad.37signals.com/authorization/new"


sso_redirect(provider="basecamp")
