import streamlit as st


def redirect_button(url):
    st.info("You have been given a Laptop Recommendation")
    st.link_button(
        "**Return to Survey** ⇒",
        url,
        type="primary",
        use_container_width=True,
    )
