from components.Auth import sso_redirect


def scopes():
    return ["openid", "profile", "email", "wso2.send_email"]


def auth_uri():
    return "https://<your-wso2-server>/oauth2/authorize"


sso_redirect(provider="wso2_identity")
