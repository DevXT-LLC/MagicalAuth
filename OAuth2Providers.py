from sso.amazon import amazon_sso
from sso.aol import aol_sso
from sso.apple import apple_sso
from sso.autodesk import autodesk_sso
from sso.basecamp import basecamp_sso
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
from sso.wso2_identity import wso2_identity_sso
from sso.xero import xero_sso
from sso.xing import xing_sso
from sso.yahoo import yahoo_sso
from sso.yammer import yammer_sso
from sso.yandex import yandex_sso
from sso.yelp import yelp_sso
from sso.zendesk import zendesk_sso


def get_sso_provider(provider: str, code, redirect_uri=None):
    if provider == "amazon":
        return amazon_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "aol":
        return aol_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "apple":
        return apple_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "autodesk":
        return autodesk_sso(code=code, redirect_uri=redirect_uri)
    elif provider == "basecamp":
        return basecamp_sso(code=code, redirect_uri=redirect_uri)
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
    elif provider == "wso2_identity":
        return wso2_identity_sso(code=code, redirect_uri=redirect_uri)
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
