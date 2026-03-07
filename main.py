import os
from dotenv import load_dotenv

from ai_model_api import AISummarizer
from email_client import EmailClient
from notification_service import NotificationService
from whatsapp_client import WhatsAppClient

load_dotenv()
USER_WHATSAPP_NUMBER = (os.getenv("WHATSAPP_NUMBER") or "").strip().replace(" ", "")


def main():
    if not USER_WHATSAPP_NUMBER:
        raise ValueError("WHATSAPP_NUMBER is missing in .env")

    email_client = EmailClient()
    whatsapp_client = WhatsAppClient()
    summarizer = AISummarizer()
    service = NotificationService(email_client, whatsapp_client, summarizer)

    email_client.connect()
    try:
        service.process_and_notify(USER_WHATSAPP_NUMBER)
    finally:
        email_client.close_connection()

if __name__ == "__main__":
    main()
