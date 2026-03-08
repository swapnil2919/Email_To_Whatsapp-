import logging
import os

from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)

class WhatsAppClient:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv("ACCOUNT_SID")
        self.auth_token = os.getenv("AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_NUMBER")
        if not self.account_sid or not self.auth_token:
            raise ValueError("ACCOUNT_SID or AUTH_TOKEN is missing in .env")
        self.client = Client(self.account_sid, self.auth_token)
        logger.info("WhatsApp client initialized.")

    @staticmethod
    def _normalize_number(number):
        if not number:
            return ""
        return str(number).strip().replace(" ", "")

    def _is_sandbox_sender(self):
        return self._normalize_number(self.twilio_number) == "+14155238886"

    def send_message(self, to_number, message_body):
        clean_from = self._normalize_number(self.twilio_number)
        clean_to = self._normalize_number(to_number)

        if not clean_from or not clean_to:
            raise ValueError("TWILIO_NUMBER or WHATSAPP_NUMBER is missing in environment.")

        try:
            message = self.client.messages.create(
                body=message_body,
                from_=f"whatsapp:{clean_from}",
                to=f"whatsapp:{clean_to}"
            )
            logger.info("Twilio message created successfully. SID=%s", message.sid)
            return {
                "sid": message.sid,
                "status": message.status,
                "error_code": message.error_code,
                "error_message": message.error_message,
                "is_sandbox": self._is_sandbox_sender(),
            }
        except TwilioRestException as exc:
            logger.exception("Twilio API request failed: %s", exc)
            return {
                "sid": None,
                "status": "failed",
                "error_code": exc.code,
                "error_message": str(exc),
                "is_sandbox": self._is_sandbox_sender(),
            }
