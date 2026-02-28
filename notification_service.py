import json

class NotificationService:
    def __init__(self, email_client, whatsapp_client):
        self.email_client = email_client
        self.whatsapp_client = whatsapp_client

    def process_and_notify(self, to_number):
        emails = self.email_client.fetch_unseen_emails()

        if not emails:
            print("No new emails.")
            return

        # Store JSON file
        with open("emails.json", "w", encoding="utf-8") as f:
            json.dump(emails, f, indent=4)
        # Format WhatsApp message
        formatted_message = self._format_message(emails)
        sid = self.whatsapp_client.send_message(to_number, formatted_message)
        print("WhatsApp sent. SID:", sid)

    def _format_message(self, emails):
        message = "📩 *New Email Notification*\n\n"
        for idx, mail in enumerate(emails, 1):
            message += (
                f"📌 *Email {idx}*\n"
                f"👤 From: {mail['from']}\n"
                f"📄 Subject: {mail['subject']}\n"
                f"📝 Body: {mail['body'][:150]}...\n"
                "----------------------\n"
            )
        return message