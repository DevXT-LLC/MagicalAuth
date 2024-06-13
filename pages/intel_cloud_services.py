from components.Auth import sso_redirect


def scopes():
    return [
        "https://api.intel.com/userinfo.read",
        "https://api.intel.com/mail.send",
    ]


def auth_uri():
    return "https://auth.intel.com/oauth2/v2.0/authorize"


sso_redirect(provider="intel_cloud_services")
