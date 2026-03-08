import os
import logging
from dotenv import load_dotenv

from ai_model_api import AISummarizer
from email_client import EmailClient
from logger_config import setup_logging
from notification_service import NotificationService
from whatsapp_client import WhatsAppClient

load_dotenv()
USER_WHATSAPP_NUMBER = (os.getenv("WHATSAPP_NUMBER") or "").strip().replace(" ", "")
logger = logging.getLogger(__name__)


def main():
    setup_logging()
    if not USER_WHATSAPP_NUMBER:
        logger.error("WHATSAPP_NUMBER is missing in .env")
        raise ValueError("WHATSAPP_NUMBER is missing in .env")

    email_client = EmailClient()
    whatsapp_client = WhatsAppClient()
    summarizer = AISummarizer()
    service = NotificationService(email_client, whatsapp_client, summarizer)

    logger.info("Email to WhatsApp job started.")
    email_client.connect()
    try:
        service.process_and_notify(USER_WHATSAPP_NUMBER)
        logger.info("Email to WhatsApp job finished.")
    except Exception:
        logger.exception("Unhandled exception during job execution.")
        raise
    finally:
        email_client.close_connection()

if __name__ == "__main__":
    main()
