import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime

class EmailClient:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("APP_PASSWORD")
        self.imap_server = os.getenv("IMAP_SERVER")
        self.connection = None

    def connect(self):
        """Establish connection to IMAP server"""
        try:
            self.connection = imaplib.IMAP4_SSL(self.imap_server)
            self.connection.login(self.email, self.password)
            print("✅ Connected successfully")
        except Exception as e:
            print("❌ Connection failed:", e)

    def fetch_unseen_emails(self):
        """Fetch today's unseen emails from Primary category"""

        self.connection.select("INBOX")

        # Get today's date in IMAP format
        today = datetime.now().strftime("%d-%b-%Y")

        status, messages = self.connection.search(
            None,
            f'(UNSEEN SINCE {today} X-GM-RAW "category:primary")'
        )

        email_ids = messages[0].split()
        email_list = []

        if not email_ids:
            print("📭 No unseen primary emails for today.")
            return

        # Get latest one only
        latest_email_id = email_ids[-1]

        res, msg_data = self.connection.fetch(latest_email_id, "(RFC822)")

        for response in msg_data:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                email_list.append(self._extract_email_data(msg))
                break

        return email_list

    def _extract_email_data(self, msg):
        """Private method to print email details with full body"""

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        from_ = msg.get("From")
        # Extract Body
        body = self._extract_body(msg)

        return {
            "from": from_,
            "subject": subject,
            "body": body[:500]  # limit body size
        }

    
    def _extract_body(self, msg):
        """Extract email body (text/plain preferred, fallback to text/html)"""

        text_body = None
        html_body = None

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # Skip attachments
                if "attachment" in content_disposition:
                    continue

                payload = part.get_payload(decode=True)
                if not payload:
                    continue

                try:
                    decoded = payload.decode()
                except:
                    continue

                if content_type == "text/plain" and not text_body:
                    text_body = decoded

                elif content_type == "text/html" and not html_body:
                    html_body = decoded

        else:
            payload = msg.get_payload(decode=True)
            if payload:
                decoded = payload.decode()
                if msg.get_content_type() == "text/plain":
                    text_body = decoded
                elif msg.get_content_type() == "text/html":
                    html_body = decoded

        # Priority: text/plain → fallback to cleaned HTML
        if text_body:
            return text_body.strip()

        if html_body:
            soup = BeautifulSoup(html_body, "html.parser")
            return soup.get_text(separator="\n").strip()

        return "No readable body found."

    def close_connection(self):
        """Close IMAP connection"""
        if self.connection:
            self.connection.close()
            self.connection.logout()
            print("🔒 Connection closed")