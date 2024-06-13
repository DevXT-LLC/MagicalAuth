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


def google_sso_button():
    client_id = getenv("GOOGLE_CLIENT_ID")
    if client_id == "":
        return ""
    code = st.query_params.get("code", "")
    if isinstance(code, list):
        code = str(code[0])
    else:
        code = str(code)
    if code == "None" or code is None:
        code = ""
    if code == "" and "token" not in st.query_params:
        scopes = urllib.parse.quote(
            "https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        )
        magic_link_uri = getenv("MAGIC_LINK_URL")
        if magic_link_uri.endswith("/"):
            magic_link_uri = magic_link_uri[:-1]
        magic_link_uri = f"{magic_link_uri}/google"
        magic_link_uri_encoded = urllib.parse.quote(magic_link_uri)
        client_id_encoded = urllib.parse.quote(client_id)
        google_sso_uri = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id_encoded}&redirect_uri={magic_link_uri_encoded}&scope={scopes}&response_type=code&access_type=offline&prompt=consent"
        with st.form("google_sso_form"):
            if st.form_submit_button("Sign in with Google", use_container_width=True):
                st.markdown(
                    f'<meta http-equiv="refresh" content="0;URL={google_sso_uri}">',
                    unsafe_allow_html=True,
                )
                st.stop()


def microsoft_sso_button():
    client_id = getenv("MICROSOFT_CLIENT_ID")
    if client_id == "":
        return ""
    code = st.query_params.get("code", "")
    if isinstance(code, list):
        code = str(code[0])
    else:
        code = str(code)
    if code == "None" or code is None:
        code = ""
    if code == "" and "token" not in st.query_params:
        scopes = urllib.parse.quote(
            "https://graph.microsoft.com/User.Read https://graph.microsoft.com/Mail.Send https://graph.microsoft.com/Calendars.ReadWrite.Shared"
        )
        magic_link_uri = getenv("MAGIC_LINK_URL")
        if magic_link_uri.endswith("/"):
            magic_link_uri = magic_link_uri[:-1]
        magic_link_uri = f"{magic_link_uri}/microsoft"
        magic_link_uri_encoded = urllib.parse.quote(magic_link_uri)
        client_id_encoded = urllib.parse.quote(client_id)
        microsoft_sso_uri = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id_encoded}&redirect_uri={magic_link_uri_encoded}&scope={scopes}&response_type=code"
        with st.form("microsoft_sso_form"):
            if st.form_submit_button(
                "Sign in with Microsoft", use_container_width=True
            ):
                st.markdown(
                    f'<meta http-equiv="refresh" content="0;URL={microsoft_sso_uri}">',
                    unsafe_allow_html=True,
                )
                st.stop()


def github_sso_button():
    client_id = getenv("GITHUB_CLIENT_ID")
    if client_id == "":
        return ""
    code = st.query_params.get("code", "")
    if isinstance(code, list):
        code = str(code[0])
    else:
        code = str(code)
    if code == "None" or code is None:
        code = ""
    if code == "" and "token" not in st.query_params:
        scopes = urllib.parse.quote("user:email read:user")
        magic_link_uri = getenv("MAGIC_LINK_URL")
        if magic_link_uri.endswith("/"):
            magic_link_uri = magic_link_uri[:-1]
        magic_link_uri = f"{magic_link_uri}/github"
        magic_link_uri_encoded = urllib.parse.quote(magic_link_uri)
        client_id_encoded = urllib.parse.quote(client_id)
        github_sso_uri = f"https://github.com/login/oauth/authorize?client_id={client_id_encoded}&redirect_uri={magic_link_uri_encoded}&scope={scopes}&response_type=code"
        with st.form("github_sso_form"):
            if st.form_submit_button("Sign in with GitHub", use_container_width=True):
                st.markdown(
                    f'<meta http-equiv="refresh" content="0;URL={github_sso_uri}">',
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
            google_sso_button()
            microsoft_sso_button()
            github_sso_button()
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
