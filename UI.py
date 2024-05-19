import streamlit as st
from MagicalAuth import MagicalAuth
import qrcode
import pyotp
import io


def login_page():
    st.write("Please login to continue.")
    new_user = st.checkbox("I am a new user")
    email = st.text_input("Email")
    if not new_user:
        otp = st.text_input("MFA Token")
        login_button = st.button("Login")
        if login_button:
            auth = MagicalAuth(email=email)
            ip_address = st.query_params.get("ip", [""])[0]
            auth_response = auth.send_magic_link(otp=otp, ip_address=ip_address)
            st.write(auth_response)
    else:
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        company_name = st.text_input("Company Name")
        job_title = st.text_input("Job Title")
        register_button = st.button("Register")
        if register_button:
            auth = MagicalAuth(email=email)
            mfa_token = auth.register(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                job_title=job_title,
            )
            totp = pyotp.TOTP(mfa_token)
            otp_uri = totp.provisioning_uri(name=email, issuer_name="MagicalAuth")
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
            mfa_confirm = st.text_input(
                "Enter the MFA token from your authenticator app"
            )
            confirm_button = st.button("Confirm MFA")
            if confirm_button:
                otp = pyotp.TOTP(mfa_token).verify(mfa_confirm)
                if otp:
                    st.success(
                        "MFA token confirmed! Please check your email for the login link."
                    )
                    st.rerun()
                else:
                    st.write("Invalid MFA token. Please try again.")
                    st.stop()


try:
    email = st.query_params["email"] if "email" in st.query_params else None
    token = st.query_params["token"] if "token" in st.query_params else None
    auth = MagicalAuth(email=email, token=token)
    user = auth.login(ip_address=st.query_params.get("ip", [""])[0])
    st.write(f"Welcome back {user.first_name}!")
except Exception as error_message:
    st.write(error_message if error_message else "Please login to continue.")
    login_page()
    st.stop()

## The rest of the code for your app goes under here...
st.title("Magical Auth")
