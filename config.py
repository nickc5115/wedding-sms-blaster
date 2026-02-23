import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    couple_names: str
    rsvp_link: str


def load_config() -> Config:
    """Load configuration from .env file and environment variables."""
    load_dotenv()

    sid = os.getenv("TWILIO_ACCOUNT_SID", "")
    token = os.getenv("TWILIO_AUTH_TOKEN", "")
    phone = os.getenv("TWILIO_PHONE_NUMBER", "")
    couple = os.getenv("COUPLE_NAMES", "")
    rsvp = os.getenv("RSVP_LINK", "")

    missing = []
    if not sid or sid == "your_account_sid_here":
        missing.append("TWILIO_ACCOUNT_SID")
    if not token or token == "your_auth_token_here":
        missing.append("TWILIO_AUTH_TOKEN")
    if not phone:
        missing.append("TWILIO_PHONE_NUMBER")

    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in your Twilio credentials.")
        sys.exit(1)

    if not couple:
        couple = "the happy couple"
    if not rsvp:
        print("Warning: RSVP_LINK not set in .env. Messages will contain an empty link.")

    return Config(
        twilio_account_sid=sid,
        twilio_auth_token=token,
        twilio_phone_number=phone,
        couple_names=couple,
        rsvp_link=rsvp,
    )
