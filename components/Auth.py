import io
import os
import time
import pyotp
import qrcode
import requests
import logging
import streamlit as st
from streamlit_js_eval import get_cookie, set_cookie
from Globals import getenv
import urllib.parse
import importlib

logging.basicConfig(
    level=getenv("LOG_LEVEL"),
    format=getenv("LOG_FORMAT"),
)

"""
Required environment variables:

- APP_NAME: Name of the application
- MAGICALAUTH_SERVER: URL of the MagicalAuth server
- MAGIC_LINK_URL: URL of the application
- GOOGLE_CLIENT_ID: Google OAuth client ID if using Google SSO
"""


def sso_buttons():
    code = st.query_params.get("code", "")
    if isinstance(code, list):
        code = str(code[0])
    else:
        code = str(code)
    if code == "None" or code is None:
        code = ""
    # For each page in pages that ends in .py, create a button
    icons = {
        "amazon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        "aol": "https://upload.wikimedia.org/wikipedia/commons/5/51/AOL.svg",
        "apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
        "autodesk": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Autodesk_logo_2019.svg",
        "basecamp": "https://upload.wikimedia.org/wikipedia/en/8/8d/Basecamp-logo.png",
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
        "wso2_identity": "https://upload.wikimedia.org/wikipedia/commons/e/ee/WSO2_Logo.svg",
        "xero": "https://images.squarespace-cdn.com/content/v1/600485aca07c94041769dbd3/1619704174874-KU8VVDKIHKB9YIS11836/XeroLogo.png",
        "xing": "https://upload.wikimedia.org/wikipedia/commons/1/17/Xing_Logo.svg",
        "yahoo": "https://s.yimg.com/rz/l/yahoo_en-US_f_p_bestfit_4x.png",
        "yammer": "https://upload.wikimedia.org/wikipedia/commons/1/11/Yammer_logo.svg",
        "yandex": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Yandex_Logo_2016.svg",
        "yelp": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Yelp_logo.svg",
        "zendesk": "https://upload.wikimedia.org/wikipedia/commons/9/91/Zendesk_logo.svg",
    }
    st.markdown(
        """
        <style>
        .sso-button {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .sso-button img {
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.form("sso_form"):
        for page in os.listdir("./pages"):
            if page.endswith(".py"):
                provider = page.split(".py")[0].lower()
                client_id = getenv(f"{provider.upper()}_CLIENT_ID")
                if client_id == "":
                    continue
                module = importlib.import_module(f"pages.{provider}")
                scopes = module.scopes()
                auth_uri = module.auth_uri()
                if code == "" and "token" not in st.query_params:
                    magic_link_uri = getenv("MAGIC_LINK_URL")
                    if magic_link_uri.endswith("/"):
                        magic_link_uri = magic_link_uri[:-1]
                    magic_link_uri = f"{magic_link_uri}/{provider}"
                    magic_link_uri_encoded = urllib.parse.quote(magic_link_uri)
                    client_id_encoded = urllib.parse.quote(client_id)
                    sso_uri = ""
                    scopes = urllib.parse.quote(" ".join(scopes))
                    sso_uri = f"{auth_uri}?client_id={client_id_encoded}&redirect_uri={magic_link_uri_encoded}&scope={scopes}&response_type=code&access_type=offline&prompt=consent"
                    if sso_uri != "":
                        if provider in icons:
                            btn_label = f'<div class="sso-button"><img src="{icons[provider]}" width="24" height="24"><span>Continue with {provider.capitalize()}</span></div>'
                        else:
                            btn_label = f"Continue with {provider.capitalize()}"
                        if st.form_submit_button(btn_label, unsafe_allow_html=True):
                            st.markdown(
                                f'<meta http-equiv="refresh" content="0;URL={sso_uri}">',
                                unsafe_allow_html=True,
                            )
                            st.stop()


def get_user():
    app_name = os.environ.get("APP_NAME", "Magical Auth")
    auth_uri = os.environ.get("MAGICALAUTH_SERVER", "http://localhost:12437")
    if "code" in st.query_params:
        if (
            st.query_params["code"] != ""
            and st.query_params["code"] is not None
            and st.query_params["code"] != "None"
        ):
            st.session_state["code"] = st.query_params["code"]
    if "code" in st.session_state:
        code = st.session_state["code"]
        if code != "" and code is not None and code != "None":
            response = requests.post(
                f"{auth_uri}/v1/oauth2/google",
                json={"code": code, "referrer": getenv("MAGIC_LINK_URL")},
            )
            if response.status_code == 200:
                data = response.json()
                if "detail" in data:
                    new_uri = data["detail"]
                    st.markdown(
                        f'<meta http-equiv="refresh" content="0;URL={new_uri}">',
                        unsafe_allow_html=True,
                    )
                    st.stop()
                else:
                    st.error(data)
                    st.stop()
    if "mfa_confirmed" in st.session_state:
        st.title(app_name)
        st.success("MFA token confirmed! Please check your email for the login link.")
        time.sleep(1)
        del st.session_state["mfa_confirmed"]
        st.stop()
    if "token" in st.query_params:
        if (
            st.query_params["token"] != ""
            and st.query_params["token"] is not None
            and st.query_params["token"] != "None"
        ):
            set_cookie("token", st.query_params["token"], 1)
            st.session_state["token"] = str(st.query_params["token"])
            st.query_params.clear()
    else:
        st.session_state["token"] = get_cookie("token")
    token = st.session_state["token"] if "token" in st.session_state else ""
    if token != "" and token is not None and token != "None":
        user_request = requests.get(
            f"{auth_uri}/v1/user",
            headers={"Authorization": token},
        )
        if user_request.status_code == 200:
            user = user_request.json()
            return user
        else:
            set_cookie("token", "", 1)
    st.title(app_name)
    if "otp_uri" in st.session_state:
        otp_uri = st.session_state["otp_uri"]
        mfa_token = str(otp_uri).split("secret=")[1].split("&")[0]
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(otp_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()
        st.write(
            "Registration successful! Please add the MFA token to your authenticator app."
        )
        with st.form("mfa_form"):
            st.image(img_bytes, caption="Scan this QR code to enable MFA")
            mfa_confirm = st.text_input(
                "Enter the MFA token from your authenticator app"
            )
            confirm_button = st.form_submit_button("Confirm MFA")
            if confirm_button:
                otp = pyotp.TOTP(mfa_token).verify(mfa_confirm)
                if otp:
                    _ = requests.post(
                        f"{auth_uri}/v1/login",
                        json={"email": st.session_state["email"], "token": mfa_confirm},
                    )
                    st.session_state["mfa_confirmed"] = True
                    if "otp_uri" in st.session_state:
                        del st.session_state["otp_uri"]
                    st.rerun()
                else:
                    st.write("Invalid MFA token. Please try again.")
                    st.stop()
    else:
        new_user = st.checkbox("I am a new user")
        if not new_user:
            with st.form("login_form"):
                email = st.text_input("Email")
                otp = st.text_input("MFA Token")
                login_button = st.form_submit_button("Login")
                if login_button:
                    auth_response = requests.post(
                        f"{auth_uri}/v1/login",
                        json={"email": email, "token": otp},
                    )
                    res = (
                        str(auth_response.json()["detail"])
                        if "detail" in auth_response.json()
                        else auth_response.json()
                    )
                    if auth_response.status_code == 200:
                        if res.startswith("http"):
                            # Redirect to the login link
                            st.markdown(
                                f'<meta http-equiv="refresh" content="0;URL={res}">',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.success(res)
                    else:
                        st.error(res)
            sso_buttons()
        else:
            with st.form("register_form"):
                email = st.text_input("Email")
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                company_name = st.text_input("Company Name")
                job_title = st.text_input("Job Title")
                register_button = st.form_submit_button("Register")
                if register_button:
                    # Make sure nothing is empty
                    if (
                        email == ""
                        or first_name == ""
                        or last_name == ""
                        or company_name == ""
                        or job_title == ""
                    ):
                        st.write("Please fill out all fields.")
                        st.stop()
                    response = requests.post(
                        f"{auth_uri}/v1/user",
                        json={
                            "email": email,
                            "first_name": first_name,
                            "last_name": last_name,
                            "company_name": company_name,
                            "job_title": job_title,
                        },
                    )
                    try:
                        mfa_token = response.json()["otp_uri"]
                    except Exception as e:
                        st.write(response.json())
                        st.stop()
                    st.session_state["email"] = email
                    st.session_state["otp_uri"] = mfa_token
                    st.rerun()
    st.stop()


def log_out_button():
    token = get_cookie("token", "logout_token")
    if token != "":
        if st.button("Log Out"):
            set_cookie("token", "", 1, "logout_set_token")
            st.query_params.clear()
            st.session_state["token"] = ""
            st.success("You have been logged out. Redirecting to login page...")
            st.markdown(
                f'<meta http-equiv="refresh" content="2;URL=/">',
                unsafe_allow_html=True,
            )
            time.sleep(2)
            st.stop()


def sso_redirect(provider: str):
    auth_uri = getenv("MAGICALAUTH_SERVER")
    if "code" in st.query_params:
        if (
            st.query_params["code"] != ""
            and st.query_params["code"] is not None
            and st.query_params["code"] != "None"
        ):
            st.session_state["code"] = st.query_params["code"]
    if "code" in st.session_state:
        code = st.session_state["code"]
        if code != "" and code is not None and code != "None":
            referrer = f"{getenv('MAGIC_LINK_URL')}/{provider}"
            response = requests.post(
                f"{auth_uri}/v1/oauth2/{provider}",
                json={"code": code, "referrer": referrer},
            )
            if response.status_code == 200:
                data = response.json()
                if "detail" in data:
                    new_uri = data["detail"]
                    st.markdown(
                        f'<meta http-equiv="refresh" content="0;URL={new_uri}">',
                        unsafe_allow_html=True,
                    )
                    st.stop()
                else:
                    st.error(data)
                    st.stop()
    if "token" in st.query_params:
        if (
            st.query_params["token"] != ""
            and st.query_params["token"] is not None
            and st.query_params["token"] != "None"
        ):
            get_user()
    if "token" not in st.query_params and "code" not in st.query_params:
        # Reload to ../ page
        st.markdown(
            f'<meta http-equiv="refresh" content="1;URL=../">',
            unsafe_allow_html=True,
        )
