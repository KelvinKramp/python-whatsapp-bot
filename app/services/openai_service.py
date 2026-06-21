import logging
import os
import shelve

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_INSTRUCTIONS = os.getenv(
    "OPENAI_INSTRUCTIONS",
    "You are having a conversation with {name}. Talk to them like a professional "
    "diabetes nurse that wants to improve their diabetes regulation. Be concise and "
    "friendly.",
)

client = OpenAI(api_key=OPENAI_API_KEY)
CONVERSATIONS_DB = "conversations_db"


def get_conversation_id(user_id: str) -> str | None:
    with shelve.open(CONVERSATIONS_DB) as db:
        return db.get(user_id)


def store_conversation_id(user_id: str, conversation_id: str) -> None:
    with shelve.open(CONVERSATIONS_DB, writeback=True) as db:
        db[user_id] = conversation_id


def ensure_conversation(user_id: str, name: str) -> str:
    conversation_id = get_conversation_id(user_id)
    if conversation_id:
        logging.info("Using conversation for %s (%s)", name, user_id)
        return conversation_id

    conversation = client.conversations.create()
    store_conversation_id(user_id, conversation.id)
    logging.info("Created conversation for %s (%s)", name, user_id)
    return conversation.id


def generate_response(message_body: str, user_id: str, name: str) -> str:
    conversation_id = ensure_conversation(user_id, name)

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=message_body,
        conversation=conversation_id,
        instructions=OPENAI_INSTRUCTIONS.format(name=name),
    )

    logging.info("Generated message for %s: %s", name, response.output_text)
    return response.output_text
