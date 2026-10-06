import streamlit as st

st.set_page_config(
    page_title="SME Cloud Security Assessment Tool",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 SME Cloud Security Assessment Tool")

st.subheader("About this prototype")

st.write(
    """
    This research prototype is designed to help small and medium-sized
    enterprises (SMEs) identify areas of cloud-security practice that may
    require further attention.
    """
)

st.info(
    """
    This tool is a questionnaire-based self-assessment aid.
    It does not certify that an organisation is secure and does not replace
    vulnerability scanning, penetration testing, formal security audits,
    or professional cybersecurity assessment.
    """
)

st.warning(
    """
    Do not enter passwords, API keys, secret keys, access tokens,
    authentication credentials, or other sensitive security information.
    """
)

st.success("Prototype successfully loaded.")
