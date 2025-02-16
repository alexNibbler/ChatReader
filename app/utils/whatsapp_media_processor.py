from flask import current_app
import requests
import logging

from app.utils.whatsapp_message_storage import get_media_directory, MessagesCollection
from app.services.genai_service import InputMessage, InputMessageType

types_supported = {
    "audio/aac" : ".aac",
    "audio/amr" : ".amr",
    "audio/mpeg" : ".mp3",
    "audio/mp4" : ".m4a",
    "audio/ogg" : ".ogg",
    "text/plain" : ".txt",
    "application/vnd.ms-excel" : ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" : ".xlsx",
    "application/msword" : ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document" : ".docx",
    "application/vnd.ms-powerpoint" : ".ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation" : ".pptx",
    "application/pdf" : ".pdf",
    "image/jpeg" : ".jpg",
    "image/png" : ".png",
}

# Videos and stickers are not supported
types_not_supported = ["image/webp", "video/3gpp", "video/mp4"]


def download_whatsapp_media(media_id, media_type, client_id) -> str | None:
    """
    Download image from WhatsApp API by the media_id and store it to the resource directory.
    :return: Path to the downloaded media file
    """
    if media_type not in types_supported:
        return None

    # Get Media URL
    media_url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{media_id}"
    headers = {"Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}"}

    response = requests.get(media_url, headers=headers)

    if response.status_code == 200:
        media_data = response.json()
        media_url = media_data.get("url")

        # Download the media file
        media_response = requests.get(media_url, headers=headers)

        # Save the media file to the resource folder
        if media_response.status_code == 200:
            file_path = f"{get_media_directory(client_id)}/whatsapp_media_{media_id}{types_supported[media_type]}"
            with open(file_path, "wb") as file:
                file.write(media_response.content)
            return file_path
        else:
            logging.warning(f"Failed to download media: {media_response.status_code}")
    else:
        logging.warning(f"Failed to fetch media URL: {response.status_code}")
    return None


def save_media(media_id: str,
               media_type: str,
               messages_collection: MessagesCollection,
               client_id: str):
    """
    Download media by media_id, save it to resources folder and add path to the messages_collection
    """
    file_path = download_whatsapp_media(media_id, media_type, client_id)
    if file_path:
        messages_collection.input_messages.append(InputMessage(type=InputMessageType.FILE_PATH,
                                                               value=file_path))