import os
import streamlit as st
from components.Auth import get_user, log_out_button

app_name = os.environ.get("APP_NAME", "Magical Auth")

st.set_page_config(
    page_title=app_name,
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded",
)

user = get_user()
st.title(app_name)
log_out_button()

## The rest of the code for your app goes under here...

st.write(f"Welcome, {user['first_name']} {user['last_name']}!")
st.write(f"About you: {user['job_title']} at {user['company_name']}")
st.write(f"Your email: {user['email']}")
