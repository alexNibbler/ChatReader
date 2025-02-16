import logging
from flask import current_app, jsonify
import json
import requests
import re

from app.services.genai_service import (process_messages_with_ai,
                                        ResponseLang,
                                        InputMessage,
                                        InputMessageType)
from app.utils.whatsapp_message_storage import (MessagesCollection,
                                                messages_storage,
                                                clear_media)
from app.utils.whatsapp_media_processor import save_media

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")

def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def generate_response(messages_collection: MessagesCollection):
    # Send query to genai
    return process_messages_with_ai(messages_collection.input_messages, MessagesCollection.lang)

def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response

def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_type = message["type"]

    if wa_id not in messages_storage.keys():
        messages_storage[wa_id] = MessagesCollection()

    messages_collection = messages_storage[wa_id]

    # Processing only text and media messages (excluding stickers and videos)
    match message_type:
        case "image" | "audio" | "document":
            # Extract media ID from webhook payload
            media_id = message[message_type]["id"]
            media_type = message[message_type]["mime_type"]
            save_media(media_id, media_type, messages_collection, wa_id)
            # Add media message caption as a separate text message
            try:
                caption = message[message_type]["caption"]
                messages_collection.input_messages.append(InputMessage(type=InputMessageType.TEXT,
                                                                       value=caption))
            except KeyError:
                ... # some messages do not have "caption" field, it's ok
            messages_collection.empty = False

        case "text":
            message_body: str = message["text"]["body"]

            send_summary: bool = False
            if re.search("^read.*english$", message_body.lower()):
                messages_collection.lang = ResponseLang.ENGLISH
                send_summary = True
            elif re.search("^read.*russian$", message_body.lower()):
                messages_collection.lang = ResponseLang.RUSSIAN
                send_summary = True
            else:
                messages_collection.input_messages.append(InputMessage(type=InputMessageType.TEXT,
                                                                       value=message_body))
                messages_collection.empty = False

            if send_summary and not messages_collection.empty:
                response = generate_response(messages_collection)
                messages_collection.input_messages.clear()
                clear_media(wa_id)
                messages_collection.empty = True
                data = get_text_message_input(wa_id, response)
                send_message(data)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
