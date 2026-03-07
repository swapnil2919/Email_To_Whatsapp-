class NotificationService:
    def __init__(self, email_client, whatsapp_client, summarizer):
        self.email_client = email_client
        self.whatsapp_client = whatsapp_client
        self.summarizer = summarizer

    def process_and_notify(self, to_number):
        emails = self.email_client.fetch_unseen_emails()
        if not emails:
            print("No new emails.")
            return

        formatted_message = self._format_message_with_summaries(emails)
        result = self.whatsapp_client.send_message(to_number, formatted_message)

        print("WhatsApp request created.")
        print("SID:", result.get("sid"))
        print("Status:", result.get("status"))
        if result.get("error_code") or result.get("error_message"):
            print("Twilio error code:", result.get("error_code"))
            print("Twilio error message:", result.get("error_message"))
        if result.get("is_sandbox"):
            print(
                "Using Twilio WhatsApp Sandbox (+14155238886). "
                "Join your WhatsApp number to sandbox by sending the Twilio join code first."
            )

    def _format_message_with_summaries(self, emails):
        message = "New email summary\n\n"
        for idx, mail in enumerate(emails, 1):
            summary = self.summarizer.summarize(str(mail.get("body", "")))
            message += (
                f"Email {idx}\n"
                f"From: {mail.get('from', '-')}\n"
                f"Subject: {mail.get('subject', '-')}\n"
                f"Summary: {summary}\n"
                "--------------------\n"
            )
        return message
