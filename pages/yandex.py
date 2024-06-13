from components.Auth import sso_redirect


def scopes():
    return [
        "login:info login:email",
        "mail.send",
    ]


def auth_uri():
    return "https://oauth.yandex.com/authorize"


sso_redirect(provider="yandex")
