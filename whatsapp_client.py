from twilio.rest import Client
import os
from dotenv import load_dotenv

class WhatsAppClient:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv("ACCOUNT_SID")
        self.auth_token = os.getenv("AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, to_number, message_body):
        message = self.client.messages.create(
            body=message_body,
            from_=f'whatsapp:{self.twilio_number}',
            to=f'whatsapp:{to_number}'
        )
        return message.sid