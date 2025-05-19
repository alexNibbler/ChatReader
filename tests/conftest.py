import pytest
import requests

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.test")

@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())

@pytest.fixture
def whatsapp_message_text() -> str:
    return '{"object": "whatsapp_business_account", "entry": [{"id": "604954029357507", "changes": [{"value": {"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15551854000", "phone_number_id": "526485007222000"}, "contacts": [{"profile": {"name": "Sender Name"}, "wa_id": "972515100000"}], "messages": [{"from": "972515100000", "id": "wamid.HBgMOTcyNTE1MTMxMDMzFQIAEhggM0JEMTM1QTcxNEM5RUFDN0FGRUE2RUQ5MEVERjI3QjYA", "timestamp": "1747604849", "text": {"body": "Read english"}, "type": "text"}]}, "field": "messages"}]}]}'

@pytest.fixture
def whatsapp_message_image() -> str:
    return '{"object": "whatsapp_business_account", "entry": [{"id": "604954029357507", "changes": [{"value": {"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15551854000", "phone_number_id": "526485007222000"}, "contacts": [{"profile": {"name": "Sender Name"}, "wa_id": "972515100000"}], "messages": [{"context": {"forwarded": "True"}, "from": "972515100000", "id": "wamid.HBgMOTcyNTE1MTMxMDMzFQIAEhggRTEyMjU0QzM0REY1Q0I4MjU1MDE5RkIzM0IwODRDRjUA", "timestamp": "1747604633", "type": "image", "image": {"mime_type": "image/jpeg", "sha256": "s/qqdfkeJBfnunsavNp7DnqEAKQy EHnC8XikOu9 EU=", "id": "1194868355287000"}}]}, "field": "messages"}]}]}'

@pytest.fixture
def whatsapp_message_audio() -> str:
    return '{"object": "whatsapp_business_account", "entry": [{"id": "604954029357507", "changes": [{"value": {"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15551854000", "phone_number_id": "526485007222000"}, "contacts": [{"profile": {"name": "Sender Name"}, "wa_id": "972515100000"}], "messages": [{"context": {"forwarded": "True"}, "from": "972515131033", "id": "wamid.HBgMOTcyNTE1MTMxMDMzFQIAEhggQURERjJFRDQyOEZBOTE1NzE2QUI0ODZGQTcwMUQ3RjQA", "timestamp": "1747662124", "type": "audio", "audio": {"mime_type": "audio/ogg; codecs=opus", "sha256": "AHA1l ar/CSUglVDTQkWKXvq C87Y6LjDxqiVhmVH3c=", "id": "1383940996185246", "voice": "False"}}]}, "field": "messages"}]}]}'