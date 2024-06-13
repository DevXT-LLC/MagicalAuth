import streamlit as st
import requests
from Globals import getenv

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
        response = requests.post(
            f"{auth_uri}/v1/oauth2/microsoft",
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
