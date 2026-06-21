import logging

from flask import Response
from twilio.twiml.messaging_response import MessagingResponse

from .whatsapp_utils import generate_response


def process_twilio_message(incoming_body, sender):
    logging.info("Twilio message from %s: %s", sender, incoming_body)
    response_text = generate_response(incoming_body)
    twiml = MessagingResponse()
    twiml.message(response_text)
    return Response(str(twiml), mimetype="text/xml")
