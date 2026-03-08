import logging


logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, email_client, whatsapp_client, summarizer):
        self.email_client = email_client
        self.whatsapp_client = whatsapp_client
        self.summarizer = summarizer

    def process_and_notify(self, to_number):
        emails = self.email_client.fetch_unseen_emails()
        if not emails:
            logger.info("No new emails to process.")
            return

        formatted_message = self._format_message_with_summaries(emails)
        result = self.whatsapp_client.send_message(to_number, formatted_message)

        logger.info("WhatsApp request created. SID=%s", result.get("sid"))
        logger.info("WhatsApp status: %s", result.get("status"))
        if result.get("error_code") or result.get("error_message"):
            logger.error(
                "Twilio error. code=%s message=%s",
                result.get("error_code"),
                result.get("error_message"),
            )
        if result.get("is_sandbox"):
            logger.warning(
                "Using Twilio WhatsApp Sandbox (+14155238886). "
                "Join your WhatsApp number to sandbox by sending the Twilio join code first."
            )

    def _format_message_with_summaries(self, emails):
        message = "New email summary\n\n"
        for idx, mail in enumerate(emails, 1):
            summary = self.summarizer.summarize(str(mail.get("body", "")))
            logger.debug("Generated summary for email %d.", idx)
            message += (
                f"Email {idx}\n"
                f"From: {mail.get('from', '-')}\n"
                f"Subject: {mail.get('subject', '-')}\n"
                f"Summary: {summary}\n"
                "--------------------\n"
            )
        return message
