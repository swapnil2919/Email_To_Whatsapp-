import email
import imaplib
import logging
import os
from datetime import datetime
from email.header import decode_header

from bs4 import BeautifulSoup
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class EmailClient:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("APP_PASSWORD")
        self.imap_server = os.getenv("IMAP_SERVER")
        self.connection = None

    def connect(self):
        """Establish connection to IMAP server."""
        try:
            if not self.email or not self.password or not self.imap_server:
                raise ValueError("EMAIL, APP_PASSWORD, or IMAP_SERVER missing in .env")
            self.connection = imaplib.IMAP4_SSL(self.imap_server)
            self.connection.login(self.email, self.password)
            logger.info("Connected to IMAP server.")
        except Exception as exc:
            logger.exception("Connection failed: %s", exc)
            self.connection = None

    def fetch_unseen_emails(self):
        """Fetch today's unseen emails from Gmail Primary category."""
        if not self.connection:
            logger.warning("No IMAP connection available. Skipping fetch.")
            return []

        self.connection.select("INBOX")
        today = datetime.now().strftime("%d-%b-%Y")
        status, messages = self.connection.search(
            None,
            f'(UNSEEN SINCE {today} X-GM-RAW "category:primary")',
        )
        if status != "OK":
            logger.error("Error searching emails. IMAP status: %s", status)
            return []

        email_ids = messages[0].split()
        if not email_ids:
            logger.info("No unseen primary emails for today.")
            return []

        logger.info("Found %d unseen email(s).", len(email_ids))
        email_list = []
        for email_id in email_ids:
            _, msg_data = self.connection.fetch(email_id, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    email_list.append(self._extract_email_data(msg))
            self.connection.store(email_id, "+FLAGS", "\\Seen")

        logger.info("Fetched and marked %d email(s) as seen.", len(email_list))
        return email_list

    def _extract_email_data(self, msg):
        subject_header = msg.get("Subject", "")
        subject, encoding = decode_header(subject_header)[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

        return {
            "from": msg.get("From", "-"),
            "subject": subject if subject else "-",
            "body": self._extract_body(msg)[:4000],
        }

    def _extract_body(self, msg):
        text_body = None
        html_body = None

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                payload = part.get_payload(decode=True)
                if not payload:
                    continue
                decoded = payload.decode(errors="ignore")
                if content_type == "text/plain" and not text_body:
                    text_body = decoded
                elif content_type == "text/html" and not html_body:
                    html_body = decoded
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                decoded = payload.decode(errors="ignore")
                if msg.get_content_type() == "text/plain":
                    text_body = decoded
                elif msg.get_content_type() == "text/html":
                    html_body = decoded

        if text_body:
            return text_body.strip()
        if html_body:
            soup = BeautifulSoup(html_body, "html.parser")
            return soup.get_text(separator="\n").strip()
        return "No readable body found."

    def close_connection(self):
        """Close IMAP connection."""
        if self.connection:
            self.connection.close()
            self.connection.logout()
            logger.info("IMAP connection closed.")
