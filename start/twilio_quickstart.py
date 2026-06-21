import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_WHATSAPP_FROM")
to_number = os.getenv("TWILIO_WHATSAPP_TO")

if not all([account_sid, auth_token, to_number]):
    raise SystemExit(
        "Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_TO in .env"
    )

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_=from_number,
    body="Lets ROLE!!!",
    to=to_number,
)

print(f"Sent message SID: {message.sid}")
