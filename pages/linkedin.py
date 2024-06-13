from components.Auth import sso_redirect


def scopes():
    return [
        "r_liteprofile",
        "r_emailaddress",
        "w_member_social",
    ]


def auth_uri():
    return "https://www.linkedin.com/oauth/v2/authorization"


sso_redirect(provider="linkedin")
