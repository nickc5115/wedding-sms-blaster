import time

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from config import Config


def create_client(config: Config) -> Client:
    return Client(config.twilio_account_sid, config.twilio_auth_token)


def send_sms(
    client: Client,
    from_number: str,
    to_number: str,
    body: str,
) -> tuple[bool, str]:
    """
    Send a single SMS. Returns (success, message_sid_or_error).
    """
    try:
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number,
        )
        return True, message.sid
    except TwilioRestException as e:
        return False, str(e)


def send_blast(
    client: Client,
    from_number: str,
    recipients: list[tuple[str, str, str]],
    delay: float = 1.0,
    progress_callback=None,
) -> list[dict]:
    """
    Send SMS to multiple recipients.

    recipients: list of (name, phone, message_body) tuples
    delay: seconds between sends to avoid throttling
    progress_callback: optional callable(index, total, name, success, detail)

    Returns a list of result dicts.
    """
    results = []
    total = len(recipients)

    for i, (name, phone, body) in enumerate(recipients):
        success, detail = send_sms(client, from_number, phone, body)

        result = {
            "name": name,
            "phone": phone,
            "success": success,
            "detail": detail,
        }
        results.append(result)

        if progress_callback:
            progress_callback(i + 1, total, name, success, detail)

        if i < total - 1:
            time.sleep(delay)

    return results
