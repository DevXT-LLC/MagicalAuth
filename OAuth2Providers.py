from sso.amazon import amazon_sso
from sso.aol import aol_sso
from sso.apple import apple_sso
from sso.autodesk import autodesk_sso
from sso.battlenet import battlenet_sso
from sso.bitbucket import bitbucket_sso
from sso.bitly import bitly_sso
from sso.clearscore import clearscore_sso
from sso.cloud_foundry import cloud_foundry_sso
from sso.deutsche_telekom import deutsche_telekom_sso
from sso.deviantart import deviantart_sso
from sso.discord import discord_sso
from sso.dropbox import dropbox_sso
from sso.facebook import facebook_sso
from sso.fatsecret import fatsecret_sso
from sso.fitbit import fitbit_sso
from sso.formstack import formstack_sso
from sso.foursquare import foursquare_sso
from sso.github import github_sso
from sso.gitlab import gitlab_sso
from sso.google import google_sso
from sso.huddle import huddle_sso
from sso.imgur import imgur_sso
from sso.instagram import instagram_sso
from sso.intel_cloud_services import intel_cloud_services_sso
from sso.jive import jive_sso
from sso.keycloak import keycloak_sso
from sso.linkedin import linkedin_sso
from sso.microsoft import microsoft_sso
from sso.netiq import netiq_sso
from sso.okta import okta_sso
from sso.openam import openam_sso
from sso.openstreetmap import openstreetmap_sso
from sso.orcid import orcid_sso
from sso.paypal import paypal_sso
from sso.ping_identity import ping_identity_sso
from sso.pixiv import pixiv_sso
from sso.reddit import reddit_sso
from sso.salesforce import salesforce_sso
from sso.sina_weibo import sina_weibo_sso
from sso.spotify import spotify_sso
from sso.stack_exchange import stack_exchange_sso
from sso.strava import strava_sso
from sso.stripe import stripe_sso
from sso.twitch import twitch_sso
from sso.viadeo import viadeo_sso
from sso.vimeo import vimeo_sso
from sso.vk import vk_sso
from sso.wechat import wechat_sso
from sso.withings import withings_sso
from sso.xero import xero_sso
from sso.xing import xing_sso
from sso.yahoo import yahoo_sso
from sso.yammer import yammer_sso
from sso.yandex import yandex_sso
from sso.yelp import yelp_sso
from sso.zendesk import zendesk_sso
from Globals import getenv


def get_sso_provider(provider: str, code, redirect_uri=None):
    if provider == "amazon":
        return amazon_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "aol":
        return aol_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "apple":
        return apple_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "autodesk":
        return autodesk_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "battlenet":
        return battlenet_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "bitbucket":
        return bitbucket_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "bitly":
        return bitly_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "clearscore":
        return clearscore_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "cloud_foundry":
        return cloud_foundry_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "deutsche_telekom":
        return deutsche_telekom_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "deviantart":
        return deviantart_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "discord":
        return discord_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "dropbox":
        return dropbox_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "facebook":
        return facebook_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "fatsecret":
        return fatsecret_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "fitbit":
        return fitbit_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "formstack":
        return formstack_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "foursquare":
        return foursquare_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "github":
        return github_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "gitlab":
        return gitlab_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "google":
        return google_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "huddle":
        return huddle_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "imgur":
        return imgur_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "instagram":
        return instagram_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "intel_cloud_services":
        return intel_cloud_services_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "jive":
        return jive_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "keycloak":
        return keycloak_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "linkedin":
        return linkedin_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "microsoft":
        return microsoft_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "netiq":
        return netiq_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "okta":
        return okta_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "openam":
        return openam_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "openstreetmap":
        return openstreetmap_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "orcid":
        return orcid_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "paypal":
        return paypal_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "ping_identity":
        return ping_identity_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "pixiv":
        return pixiv_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "reddit":
        return reddit_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "salesforce":
        return salesforce_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "sina_weibo":
        return sina_weibo_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "spotify":
        return spotify_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "stack_exchange":
        return stack_exchange_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "strava":
        return strava_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "stripe":
        return stripe_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "twitch":
        return twitch_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "viadeo":
        return viadeo_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "vimeo":
        return vimeo_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "vk":
        return vk_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "wechat":
        return wechat_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "withings":
        return withings_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "xero":
        return xero_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "xing":
        return xing_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "yahoo":
        return yahoo_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "yammer":
        return yammer_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "yandex":
        return yandex_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "yelp":
        return yelp_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "zendesk":
        return zendesk_sso(code=code, redirect_uri=redirect_uri)
    else:
        return None


def get_scopes(provider):
    scope = {
        "amazon": ["openid", "email", "profile"],
        "aol": [
            "https://api.aol.com/userinfo.profile",
            "https://api.aol.com/userinfo.email",
            "https://api.aol.com/mail.send",
        ],
        "apple": ["name", "email"],
        "autodesk": ["data:read", "data:write", "bucket:read", "bucket:create"],
        "battlenet": ["openid", "email"],
        "bitbucket": ["account", "email"],
        "bitly": ["bitly:read", "bitly:write"],
        "clearscore": ["user.info.read", "email.send"],
        "cloud_foundry": ["cloud_controller.read", "openid", "email"],
        "deutsche_telekom": ["t-online-profile", "t-online-email"],
        "deviantart": ["user", "browse", "stash", "send_message"],
        "discord": ["identify", "email"],
        "dropbox": ["account_info.read", "files.metadata.read"],
        "facebook": ["public_profile", "email", "pages_messaging"],
        "fatsecret": ["profile.get"],
        "fitbit": [
            "activity",
            "heartrate",
            "location",
            "nutrition",
            "profile",
            "settings",
            "sleep",
            "social",
            "weight",
        ],
        "formstack": ["formstack:read", "formstack:write"],
        "foursquare": [],
        "github": ["user:email", "read:user"],
        "gitlab": ["read_user", "api", "email"],
        "google": [
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
        ],
        "huddle": ["user_info", "send_email"],
        "imgur": ["read", "write"],
        "instagram": ["user_profile", "user_media"],
        "intel_cloud_services": [
            "https://api.intel.com/userinfo.read",
            "https://api.intel.com/mail.send",
        ],
        "jive": ["your_required_scopes_here"],
        "keycloak": ["openid", "email", "profile"],
        "linkedin": ["r_liteprofile", "r_emailaddress", "w_member_social"],
        "microsoft": [
            "https://graph.microsoft.com/User.Read https://graph.microsoft.com/Mail.Send",
            "https://graph.microsoft.com/Calendars.ReadWrite.Shared",
        ],
        "netiq": ["profile", "email", "openid", "user.info"],
        "okta": ["openid", "profile", "email"],
        "openam": ["profile", "email"],
        "openstreetmap": ["read_prefs"],
        "orcid": ["/authenticate", "/activities/update"],
        "paypal": ["email openid"],
        "ping_identity": ["profile", "email", "openid"],
        "pixiv": ["pixiv.scope.profile.read"],
        "reddit": ["identity", "submit", "read"],
        "salesforce": ["refresh_token full email"],
        "sina_weibo": ["email", "statuses_update"],
        "spotify": ["user-read-email", "user-read-private", "playlist-read-private"],
        "stack_exchange": ["read_inbox no_expiry private_info write_access"],
        "strava": ["read", "activity:write"],
        "stripe": ["read_write"],
        "twitch": ["user:read:email"],
        "viadeo": ["basic", "email"],
        "vimeo": ["public", "private", "video_files"],
        "vk": ["email"],
        "wechat": ["snsapi_userinfo"],
        "withings": ["user.info", "user.metrics", "user.activity"],
        "xero": ["openid", "profile", "email", "offline_access"],
        "xing": [
            "https://api.xing.com/v1/users/me",
            "https://api.xing.com/v1/authorize",
        ],
        "yahoo": ["profile", "email", "mail-w"],
        "yammer": ["messages:email", "messages:post"],
        "yandex": ["login:info login:email", "mail.send"],
        "yelp": ["business"],
        "zendesk": ["read", "write"],
    }
    return scope[provider] if provider in scope else None


def get_authorization_url(provider):
    uris = {
        "amazon": f"https://{getenv('AWS_USER_POOL_ID')}.auth.{getenv('AWS_REGION')}.amazoncognito.com/oauth2/authorize",
        "aol": "https://api.login.aol.com/oauth2/authorize",
        "apple": "https://appleid.apple.com/auth/authorize",
        "autodesk": "https://developer.api.autodesk.com/authentication/v1/authorize",
        "battlenet": "https://oauth.battle.net/authorize",
        "bitbucket": "https://bitbucket.org/site/oauth2/authorize",
        "bitly": "https://bitly.com/oauth/authorize",
        "clearscore": "https://auth.clearscore.com/oauth2/authorize",
        "cloud_foundry": "https://login.system.example.com/oauth/authorize",
        "deutsche_telekom": "https://www.telekom.com/ssoservice/authorize",
        "deviantart": "https://www.deviantart.com/oauth2/authorize",
        "discord": "https://discord.com/api/oauth2/authorize",
        "dropbox": "https://www.dropbox.com/oauth2/authorize",
        "facebook": "https://www.facebook.com/v10.0/dialog/oauth",
        "fatsecret": "https://oauth.fatsecret.com/connect/authorize",
        "fitbit": "https://www.fitbit.com/oauth2/authorize",
        "formstack": "https://www.formstack.com/api/v2/oauth2/authorize",
        "foursquare": "https://foursquare.com/oauth2/authenticate",
        "github": "https://github.com/login/oauth/authorize",
        "gitlab": "https://gitlab.com/oauth/authorize",
        "google": "https://accounts.google.com/o/oauth2/auth",
        "huddle": "https://login.huddle.com/oauth2/authorize",
        "imgur": "https://api.imgur.com/oauth2/authorize",
        "instagram": "https://api.instagram.com/oauth/authorize",
        "intel_cloud_services": "https://auth.intel.com/oauth2/v2.0/authorize",
        "jive": "https://example.jive.com/oauth2/authorize",
        "keycloak": "https://your-keycloak-server/auth/realms/your-realm/protocol/openid-connect/auth",
        "linkedin": "https://www.linkedin.com/oauth/v2/authorization",
        "microsoft": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "netiq": "https://your-netiq-domain.com/oauth2/authorize",
        "okta": "https://your-okta-domain/oauth2/v1/authorize",
        "openam": "https://your-openam-base-url/oauth2/authorize",
        "openstreetmap": "https://www.openstreetmap.org/oauth/authorize",
        "orcid": "https://orcid.org/oauth/authorize",
        "paypal": "https://www.paypal.com/signin/authorize",
        "ping_identity": "https://auth.pingidentity.com/as/authorize.oauth2",
        "pixiv": "https://oauth.secure.pixiv.net/auth/authorize",
        "reddit": "https://www.reddit.com/api/v1/authorize",
        "salesforce": "https://login.salesforce.com/services/oauth2/authorize",
        "sina_weibo": "https://api.weibo.com/oauth2/authorize",
        "spotify": "https://accounts.spotify.com/authorize",
        "stack_exchange": "https://stackexchange.com/oauth",
        "strava": "https://www.strava.com/oauth/authorize",
        "stripe": "https://connect.stripe.com/oauth/authorize",
        "twitch": "https://id.twitch.tv/oauth2/authorize",
        "viadeo": "https://secure.viadeo.com/oauth-provider/authorize",
        "vimeo": "https://api.vimeo.com/oauth/authorize",
        "vk": "https://oauth.vk.com/authorize",
        "wechat": "https://open.weixin.qq.com/connect/qrconnect",
        "withings": "https://account.withings.com/oauth2_user/authorize2",
        "xero": "https://login.xero.com/identity/connect/authorize",
        "xing": "https://api.xing.com/v1/authorize",
        "yahoo": "https://api.login.yahoo.com/oauth2/request_auth",
        "yammer": "https://www.yammer.com/oauth2/authorize",
        "yandex": "https://oauth.yandex.com/authorize",
        "yelp": "https://api.yelp.com/oauth2/authorize",
        "zendesk": f"https://{getenv('ZENDESK_SUBDOMAIN')}.zendesk.com/oauth/authorizations/new",
    }
    return uris[provider] if provider in uris else None


def get_icon(provider):
    icons = {
        "amazon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        "aol": "https://upload.wikimedia.org/wikipedia/commons/5/51/AOL.svg",
        "apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
        "autodesk": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Autodesk_logo_2019.svg",
        "battlenet": "https://upload.wikimedia.org/wikipedia/en/1/1b/Battle.net_Icon.svg",
        "bitbucket": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Bitbucket-blue-logomark-only.svg",
        "bitly": "https://upload.wikimedia.org/wikipedia/commons/5/56/Bitly_logo.svg",
        "clearscore": "https://upload.wikimedia.org/wikipedia/en/5/57/ClearScore_logo.png",
        "cloud_foundry": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Cloud_Foundry_Logo.svg/512px-Cloud_Foundry_Logo.svg.png",
        "deutsche_telekom": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Logo_telekom_2013.svg",
        "deviantart": "https://upload.wikimedia.org/wikipedia/commons/b/b5/DeviantArt_Logo.svg",
        "discord": "https://upload.wikimedia.org/wikipedia/commons/9/98/Discord_logo.svg",
        "dropbox": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Dropbox_Icon.svg",
        "facebook": "https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg",
        "fatsecret": "https://upload.wikimedia.org/wikipedia/en/2/20/FatSecret.png",
        "fitbit": "https://upload.wikimedia.org/wikipedia/commons/6/60/Fitbit_logo_2016.svg",
        "formstack": "https://upload.wikimedia.org/wikipedia/en/0/09/Formstack_logo.png",
        "foursquare": "https://upload.wikimedia.org/wikipedia/en/1/12/Foursquare_logo.svg",
        "github": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg",
        "gitlab": "https://upload.wikimedia.org/wikipedia/commons/1/18/GitLab_Logo.svg",
        "google": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Google-favicon-2015.png",
        "imgur": "https://upload.wikimedia.org/wikipedia/en/a/a9/Imgur_logo.svg",
        "instagram": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png",
        "intel_cloud_services": "https://corporate-intelcom.azureedge.net/assets/Intel-Logo.svg",
        "jive": "https://upload.wikimedia.org/wikipedia/en/8/8a/Jive_logo.png",
        "keycloak": "https://www.keycloak.org/resources/images/keycloak_logo_400x.png",
        "linkedin": "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png",
        "microsoft": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
        "netiq": "https://upload.wikimedia.org/wikipedia/commons/3/30/NetIQ_logo.svg",
        "okta": "https://upload.wikimedia.org/wikipedia/commons/5/50/Okta_Logo_Brandmark_Blue_RGB.png",
        "openam": "https://avatars.githubusercontent.com/u/383598?v=4",
        "openstreetmap": "https://upload.wikimedia.org/wikipedia/commons/6/66/OpenStreetMap-Logo.svg",
        "orcid": "https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg",
        "paypal": "https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg",
        "ping_identity": "https://upload.wikimedia.org/wikipedia/en/e/e2/Ping_Identity_logo.jpg",
        "pixiv": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Pixiv_comic_icon.svg",
        "reddit": "https://upload.wikimedia.org/wikipedia/en/8/82/Reddit_logo_and_wordmark.svg",
        "salesforce": "https://upload.wikimedia.org/wikipedia/en/b/b5/Salesforce_logo_transparent.png",
        "spotify": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
        "stack_exchange": "https://upload.wikimedia.org/wikipedia/commons/2/28/Stack_Exchange_logo.svg",
        "strava": "https://upload.wikimedia.org/wikipedia/en/0/0d/Strava_Logo.svg",
        "stripe": "https://upload.wikimedia.org/wikipedia/commons/3/3b/Stripe_Logo%2C_revised_2016.png",
        "twitch": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Twitch_logo_2019.svg",
        "vimeo": "https://upload.wikimedia.org/wikipedia/commons/9/92/Vimeo_Logo.svg",
        "vk": "https://upload.wikimedia.org/wikipedia/commons/2/21/VK.com-logo.svg",
        "wechat": "https://upload.wikimedia.org/wikipedia/commons/9/9e/WeChat_Logo.svg",
        "withings": "https://upload.wikimedia.org/wikipedia/en/a/a7/Withings_logo.svg",
        "xero": "https://images.squarespace-cdn.com/content/v1/600485aca07c94041769dbd3/1619704174874-KU8VVDKIHKB9YIS11836/XeroLogo.png",
        "xing": "https://upload.wikimedia.org/wikipedia/commons/1/17/Xing_Logo.svg",
        "yahoo": "https://s.yimg.com/rz/l/yahoo_en-US_f_p_bestfit_4x.png",
        "yammer": "https://upload.wikimedia.org/wikipedia/commons/1/11/Yammer_logo.svg",
        "yandex": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Yandex_Logo_2016.svg",
        "yelp": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Yelp_logo.svg",
        "zendesk": "https://upload.wikimedia.org/wikipedia/commons/9/91/Zendesk_logo.svg",
    }
    return icons[provider] if provider in icons else None
