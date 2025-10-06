import streamlit as st
from twilio.rest import Client

def send_otp(phone_number: str) -> bool:
    """Send OTP using Twilio Verify API"""
    try:
        # Initialize Twilio client from Streamlit secrets
        client = Client(
            st.secrets["twilio"]["account_sid"],
            st.secrets["twilio"]["auth_token"]
        )

        # Start verification via SMS
        verification = client.verify \
            .services(st.secrets["twilio"]["verify_sid"]) \
            .verifications \
            .create(to=phone_number, channel="sms")

        return verification.status == "pending"

    except Exception as e:
        st.error(f"❌ Error sending OTP: {e}")
        return False


def verify_otp(phone_number: str, otp_code: str) -> bool:
    """Verify the OTP entered by the user"""
    try:
        # Initialize Twilio client from Streamlit secrets
        client = Client(
            st.secrets["twilio"]["account_sid"],
            st.secrets["twilio"]["auth_token"]
        )

        # Check verification
        verification_check = client.verify \
            .services(st.secrets["twilio"]["verify_sid"]) \
            .verification_checks \
            .create(to=phone_number, code=otp_code)

        return verification_check.status == "approved"

    except Exception as e:
        st.error(f"❌ Error verifying OTP: {e}")
        return Fals
