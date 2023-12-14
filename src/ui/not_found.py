import streamlit as st


def not_found():
    st.markdown("# Hey :wave:")
    st.markdown(
        "This is our test chat client for the Advanced NLP Project at the University of Twente."
    )
    st.markdown(
        "Unfortunately, the link you entered does not correspond to one of our experiments. :test_tube: :thinking_face:"
    )
    st.markdown("---")
    st.markdown(
        "### Contact Us \n write us a message if you did not expect to see this page."
    )
    st.markdown("+ [Mark Bruderer](mailto:m.a.bruderervanblerk@student.utwente.nl)")
    st.stop()
