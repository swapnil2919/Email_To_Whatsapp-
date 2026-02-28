# Email_To_Whatsapp-
Email_To_Whatsapp is a Python automation project that reads incoming emails using the imaplib library and forwards the email content directly to WhatsApp using the Twilio API.


# Email to WhatsApp Notification Bot

This project monitors incoming emails using IMAP and sends a WhatsApp notification using Twilio whenever a new email is received.

## 🚀 Features

- Connects to Gmail using IMAP
- Detects new unread emails
- Extracts subject and sender
- Sends WhatsApp notification via Twilio
- Uses environment variables for security

---

## 🛠 Tech Stack

- Python
- IMAP (Email reading)
- Twilio API (WhatsApp messaging)
- dotenv (Environment variable management)

---

## 📁 Project Structure

email-whatsapp-bot/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md

---

## 🔐 Environment Variables Setup

Create a `.env` file and add:

EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password
IMAP_SERVER=imap.gmail.com

ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
TWILIO_NUMBER=whatsapp:+14155238886
WHATSAPP_NUMBER=whatsapp:+91xxxxxxxxxx

⚠️ Do NOT upload `.env` to GitHub.

---

## 📦 Installation

```bash
pip install -r requirements.txt

Run the Project
python main.py
