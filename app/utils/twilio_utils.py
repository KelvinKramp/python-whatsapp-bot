import logging

from flask import Response
from twilio.twiml.messaging_response import MessagingResponse

from app.services.openai_service import generate_response
from app.utils.whatsapp_utils import process_text_for_whatsapp


def process_twilio_message(incoming_body, sender):
    logging.info("Twilio message from %s: %s", sender, incoming_body)
    response_text = generate_response(incoming_body, sender, sender)
    logging.info("Response text: %s", response_text)
    response_text = process_text_for_whatsapp(response_text)
    logging.info("Response text after processing: %s", response_text)
    twiml = MessagingResponse()
    twiml.message(response_text)
    return Response(str(twiml), mimetype="text/xml")
