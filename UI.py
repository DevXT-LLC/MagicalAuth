import streamlit as st
from streamlit_js_eval import streamlit_js_eval, get_cookie, set_cookie
import qrcode
import pyotp
import io
import os
import requests
import time


def get_user():
    base_uri = os.environ.get("MAGICALAUTH_SERVER", "http://localhost:12437")
    email = get_cookie("email")
    token = get_cookie("token")
    print(f"session state: {st.session_state}")
    if "mfa_confirmed" in st.session_state:
        st.success("MFA token confirmed! Please check your email for the login link.")
        time.sleep(1)
        del st.session_state["mfa_confirmed"]
        st.stop()
    if "email" in st.query_params:
        set_cookie("email", st.query_params["email"], 1)
        email = st.query_params["email"]
    if "token" in st.query_params:
        set_cookie("token", st.query_params["token"], 1)
        token = st.query_params["token"]
    if token != "" and token is not None:
        user_request = requests.post(
            f"{base_uri}/login",
            json={"email": email, "token": token},
        )
        if user_request.status_code == 200:
            user = user_request.json()
            return user
        else:
            set_cookie("email", "", 1)
            set_cookie("token", "", 1)
    if "mfa_token" in st.session_state:
        mfa_token = st.session_state["mfa_token"]
        totp = pyotp.TOTP(mfa_token)
        otp_uri = totp.provisioning_uri(
            name=st.session_state["email"], issuer_name="MagicalAuth"
        )
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
        st.image(img_bytes, caption="Scan this QR code to enable MFA")
        mfa_confirm = st.text_input("Enter the MFA token from your authenticator app")
        confirm_button = st.button("Confirm MFA")
        if confirm_button:
            otp = pyotp.TOTP(mfa_token).verify(mfa_confirm)
            if otp:
                # Send magic link
                print(
                    f"Sending to {st.session_state['email']} with token {mfa_confirm}"
                )
                _ = requests.post(
                    f"{base_uri}/send_magic_link",
                    json={"email": st.session_state["email"], "token": mfa_confirm},
                )
                st.session_state["mfa_confirmed"] = True
                if "mfa_token" in st.session_state:
                    del st.session_state["mfa_token"]
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
                        f"{base_uri}/send_magic_link",
                        json={"email": email, "token": otp},
                    )
                    if auth_response.status_code == 200:
                        st.write(auth_response.json()["message"])
                    else:
                        st.write(auth_response.json())
        else:
            with st.form("register_form"):
                email = st.text_input("Email")
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                company_name = st.text_input("Company Name")
                job_title = st.text_input("Job Title")
                register_button = st.form_submit_button("Register")
                if register_button:
                    response = requests.post(
                        f"{base_uri}/register",
                        json={
                            "email": email,
                            "first_name": first_name,
                            "last_name": last_name,
                            "company_name": company_name,
                            "job_title": job_title,
                        },
                    )
                    try:
                        mfa_token = response.json()["mfa_token"]
                    except Exception as e:
                        st.write(response.json())
                        st.stop()
                    st.session_state["email"] = email
                    st.session_state["mfa_token"] = mfa_token
                    st.rerun()
    return None


def log_out():
    set_cookie("email", "", 1)
    set_cookie("token", "", 1)
    st.session_state["token"] = ""
    st.success("You have been logged out.")
    time.sleep(2)
    st.stop()


st.title("Magical Auth")
user = get_user()
if user is None:
    st.stop()

## The rest of the code for your app goes under here...
st.write(f"Welcome, {user['first_name']} {user['last_name']}!")
st.write(f"About you: {user['job_title']} at {user['company_name']}")
st.write(f"Your email: {user['email']}")

log_out_button = st.button("Log Out")
if log_out_button:
    log_out()
