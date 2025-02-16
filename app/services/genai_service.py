import os
from dataclasses import dataclass
from typing import List
from enum import Enum
from dotenv import load_dotenv
from google import genai
import logging

import app.strings.strings_en as strings

class ResponseLang(Enum):
    ENGLISH = "English"
    RUSSIAN = "Russian"

class InputMessageType(Enum):
    TEXT = 1
    FILE_PATH = 2

@dataclass
class InputMessage:
    type: InputMessageType
    value: str

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=GENAI_API_KEY)

def process_messages_with_ai(input_messages: List[InputMessage], lang: ResponseLang):
    """
    Combines the list of media and text messages into gemini prompt
    and returns the summary in the selected language
    :param input_messages - list of messages to process
    :param lang - the language of response
    :return concise summary of the input
    """
    # query_contents = ["In not more than 3 sentences tell in {lang.value} the succinct content of the following text messages and media content (if any media present):"]
    query_contents = [strings.prompt.format(lang.value)]
    for input_message in input_messages:
        match input_message.type:
            case InputMessageType.FILE_PATH:
                try:
                    media_file = client.files.upload(file=input_message.value)
                    query_contents.append(media_file)
                except FileNotFoundError:
                    logging.warning(f"Image {input_message.value} not found")
            case InputMessageType.TEXT:
                query_contents.append(input_message.value)

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=query_contents)
    return response.text
