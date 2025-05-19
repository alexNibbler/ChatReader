import pytest
import app.utils.whatsapp_utils as wa_utils
import json

def convert_json_to_dict(raw_json: str) -> dict:
    return json.loads(raw_json)

@pytest.mark.parametrize("message_fixture",
                         ["whatsapp_message_text",
                          "whatsapp_message_image",
                          "whatsapp_message_audio"])
def test_is_valid_whatsapp_message_positive(message_fixture: str, request):
    raw_message = request.getfixturevalue(message_fixture)
    valid = wa_utils.is_valid_whatsapp_message(convert_json_to_dict(raw_message))
    assert valid

@pytest.mark.parametrize("raw_message",
                         ['{"object": "whatsapp_business_account", "entry": []}',
                          "{}"])
def test_is_valid_whatsapp_message_negative(raw_message: str):
    valid = wa_utils.is_valid_whatsapp_message(convert_json_to_dict(raw_message))
    assert not valid

def test_pr(whatsapp_message_text):
    wa_utils.process_whatsapp_message(convert_json_to_dict(whatsapp_message_text))