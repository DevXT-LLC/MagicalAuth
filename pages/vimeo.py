from components.Auth import sso_redirect


def scopes():
    return [
        "public",
        "private",
        "video_files",
    ]


def auth_uri():
    return "https://api.vimeo.com/oauth/authorize"


sso_redirect(provider="vimeo")
