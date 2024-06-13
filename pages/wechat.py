from components.Auth import sso_redirect


def scopes():
    return ["snsapi_userinfo"]


def auth_uri():
    return "https://open.weixin.qq.com/connect/qrconnect"


sso_redirect(provider="wechat")
