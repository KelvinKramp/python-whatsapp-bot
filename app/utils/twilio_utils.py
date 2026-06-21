import logging

from flask import Response
from twilio.twiml.messaging_response import MessagingResponse

from .whatsapp_utils import generate_response


def process_twilio_message(incoming_body, sender):
    logging.info("Twilio message from %s: %s", sender, incoming_body)
    # response = generate_response(message_body, wa_id, name)
    # response = process_text_for_whatsapp(response)
    response_text = generate_response(incoming_body)
    twiml = MessagingResponse()
    twiml.message(response_text)
    return Response(str(twiml), mimetype="text/xml")
