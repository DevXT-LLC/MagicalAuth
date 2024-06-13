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
"""


def google_sso_button():
    client_id = getenv("GOOGLE_CLIENT_ID")
    if client_id == "":
        return ""
    auth_uri = getenv("MAGICALAUTH_SERVER")
    magic_link_uri = getenv("MAGIC_LINK_URL")
    if magic_link_uri.endswith("/"):
        magic_link_uri = magic_link_uri[:-1]
    authorize_endpoint = "https://accounts.google.com/o/oauth2/auth"
    scopes = "https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    result = st.button("Sign in with Google", key="google_sso_button")
    if result and "code" not in st.query_params:
        scopes = urllib.parse.quote(scopes)
        magic_link_uri = urllib.parse.quote(magic_link_uri)
        client_id = urllib.parse.quote(client_id)
        new_uri = f"{authorize_endpoint}?client_id={client_id}&redirect_uri={magic_link_uri}&scope={scopes}&response_type=code&access_type=offline&prompt=consent"
        # Redirect to Google SSO
        st.markdown(
            f'<meta http-equiv="refresh" content="0;URL={new_uri}">',
            unsafe_allow_html=True,
        )
    if "code" in st.query_params:
        if st.query_params["code"] != "":
            code = str(st.query_params["code"])
            logging.info(f"Saving code: {code}")
            # save the code in the cookie
            set_cookie("code", code, 1, "set_code_cookie")
            # Clear code from URL
            st.query_params["code"] = ""
            st.query_params["scope"] = ""
            st.query_params["state"] = ""
            st.query_params["authuser"] = ""
            st.query_params["prompt"] = ""
            st.markdown(
                f'<meta http-equiv="refresh" content="0;URL=/">',
                unsafe_allow_html=True,
            )
    # Get cookie of "code", if it exists
    code = get_cookie("code", "get_code_cookie")
    if code != "" and code is not None:
        logging.info(f"Referencing code: {code}")
        response = requests.post(
            f"{auth_uri}/v1/oauth2/google",
            json={
                "code": code,
                "referrer": magic_link_uri,
            },
        )
        res = response.json()
        if "detail" in res:
            details = res["detail"]
            logging.info(f"Google SSO Detail: {details}")
            if str(details).startswith("http"):
                set_cookie("code", "", 1, "clear_code_cookie")
                # Go to the login link
                st.markdown(
                    f'<meta http-equiv="refresh" content="0;URL={details}">',
                    unsafe_allow_html=True,
                )
            else:
                st.error(details)
                logging.error(f"Error with Google SSO: {details}")
        else:
            st.error(response.text)
            logging.error(f"Error with Google SSO: {response.text}")


def get_user():
    app_name = os.environ.get("APP_NAME", "Magical Auth")
    auth_uri = os.environ.get("MAGICALAUTH_SERVER", "http://localhost:12437")
    email = get_cookie("email")
    token = get_cookie("token")
    if "mfa_confirmed" in st.session_state:
        st.title(app_name)
        st.success("MFA token confirmed! Please check your email for the login link.")
        time.sleep(1)
        del st.session_state["mfa_confirmed"]
        st.stop()
    if "email" in st.query_params:
        if st.query_params["email"] != "" and st.query_params["email"] is not None:
            set_cookie("email", st.query_params["email"], 1)
            email = st.query_params["email"]
    if "token" in st.query_params:
        if st.query_params["token"] != "" and st.query_params["token"] is not None:
            set_cookie("token", st.query_params["token"], 1)
            token = st.query_params["token"]
    if token != "" and token is not None:
        user_request = requests.get(
            f"{auth_uri}/v1/user",
            headers={"Authorization": token},
        )
        if user_request.status_code == 200:
            user = user_request.json()
            return user
        else:
            set_cookie("email", "", 1)
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
            set_cookie("email", "", 1, "logout_set_email")
            set_cookie("token", "", 1, "logout_set_token")
            st.query_params["email"] = ""
            st.query_params["token"] = ""
            st.session_state["token"] = ""
            st.success("You have been logged out. Redirecting to login page...")
            st.markdown(
                f'<meta http-equiv="refresh" content="2;URL=/">',
                unsafe_allow_html=True,
            )
            time.sleep(2)
            st.stop()
