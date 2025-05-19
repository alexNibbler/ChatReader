from dataclasses import dataclass, field
from typing import List, Dict
from pathlib import Path
import shutil
import logging
import os

from app.services.genai_service import InputMessage, ResponseLang


@dataclass
class MessagesCollection:
    input_messages: List[InputMessage] = field(default_factory=list)
    lang: ResponseLang = ResponseLang.ENGLISH
    empty: bool = True
    is_media_downloading: bool = False
    media_ready_notification_required: bool = False

def get_media_directory(client_id: str = None):
    if client_id:
        path_str = f'media/{client_id.strip("+")}'
        path = Path(path_str)
        path.mkdir(parents=True, exist_ok=True)
        return path_str
    return "media"

def clear_media(client_id: str = None):
    """
    Removes all files in the media directory.
    If client_id param is specified only media for the given client are removed
    """
    directory = get_media_directory(client_id)
    path = Path(directory)

    if path.exists():
        try:
            shutil.rmtree(path)
        except Exception as ex:
            logging.warning(f"Temp media directory '{directory}' could not be removed: {ex}")
    else:
        logging.warning(f"Temp media directory '{directory}' not found and cannot be cleared.")


messages_storage: Dict[str, MessagesCollection] = {}
clear_media()