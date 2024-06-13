from components.Auth import sso_redirect


def scopes():
    return [
        "email openid",
    ]


def auth_uri():
    return "https://www.paypal.com/signin/authorize"  # Ensure this is the correct authorization URL for PayPal


sso_redirect(provider="paypal")
