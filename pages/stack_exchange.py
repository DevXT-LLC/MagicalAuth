from components.Auth import sso_redirect


def scopes():
    return ["read_inbox no_expiry private_info write_access"]


def auth_uri():
    return "https://stackexchange.com/oauth"


sso_redirect(provider="stack_exchange")
