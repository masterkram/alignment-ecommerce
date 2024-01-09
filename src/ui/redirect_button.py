import streamlit as st


def redirect_button(url, info):
    text = ""
    if info == "recommended":
        text = "You have been recommended a laptop. Please click on the button below to return to the survey."
    elif info == "long":
        text = "The conversation has unfortunately taken too many turns. Please click on the button below to return to the survey."

    st.balloons()
    st.info(text)
    st.link_button(
        "**Return to Survey** ⇒",
        url,
        type="primary",
        use_container_width=True,
    )
