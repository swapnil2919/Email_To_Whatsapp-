import os
from email_client import EmailClient
from whatsapp_client import WhatsAppClient
from notification_service import NotificationService
from dotenv import load_dotenv

load_dotenv()
USER_WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")
def main():
    email_client = EmailClient()
    whatsapp_client = WhatsAppClient()
    email_client.connect()
    service = NotificationService(email_client, whatsapp_client)
    service.process_and_notify(USER_WHATSAPP_NUMBER)

    email_client.close_connection()

if __name__ == "__main__":
    main()