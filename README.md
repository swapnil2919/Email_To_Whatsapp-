# Email to WhatsApp AI Summary Bot

This project reads unread Gmail emails using IMAP, creates a short AI summary, and sends that summary to WhatsApp through Twilio.

## Features
- Fetches today's unseen emails from Gmail Primary inbox
- Extracts readable body text from plain text/HTML emails
- Summarizes email content using Hugging Face inference API
- Sends compact summaries to WhatsApp via Twilio
- Uses OOP-based service structure for maintainability

## Project Structure
- `main.py` - app entrypoint
- `email_client.py` - IMAP email reader
- `ai_model_api.py` - `AISummarizer` class
- `notification_service.py` - orchestration and formatting
- `whatsapp_client.py` - Twilio WhatsApp sender

## Environment Variables
Add these values to `.env`:

```env
EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password
IMAP_SERVER=imap.gmail.com

ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
TWILIO_NUMBER=+14155238886
WHATSAPP_NUMBER=+91xxxxxxxxxx

HUGGING_FACE_TOKEN=your_huggingface_token
```

If `HUGGING_FACE_TOKEN` is missing, the app falls back to a shortened plain-text extract instead of AI summary.

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```
