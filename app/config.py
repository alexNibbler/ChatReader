import sys
import os
from dotenv import load_dotenv
import logging


def load_configurations(app):
    load_dotenv()
    app.config["ACCESS_TOKEN"] = os.getenv("ACCESS_TOKEN")
    app.config["YOUR_PHONE_NUMBER"] = os.getenv("YOUR_PHONE_NUMBER")
    app.config["APP_ID"] = os.getenv("APP_ID")
    app.config["APP_SECRET"] = os.getenv("APP_SECRET")
    app.config["RECIPIENT_WAID"] = os.getenv("RECIPIENT_WAID")
    app.config["VERSION"] = os.getenv("VERSION")
    app.config["PHONE_NUMBER_ID"] = os.getenv("PHONE_NUMBER_ID")
    app.config["VERIFY_TOKEN"] = os.getenv("VERIFY_TOKEN")


def configure_logging():
    """
    1. Set verbose level according to env variable DEBUG_MODE
    2. Set format of the log as <date> <log_level> <module>: <message>
    3. Levels INFO and below are sent to stdout, WARNING and above to stderr
    """
    dev_mode = os.getenv("DEBUG_MODE").lower() in ["true", "yes", "dev", "debug", "verbose"]
    log_level = logging.DEBUG if dev_mode else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(module)s: %(message)s")

    _logger = logging.getLogger()

    # log lower levels to stdout
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)
    _logger.addHandler(stdout_handler)

    # log higher levels to stderr (red)
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.addFilter(lambda rec: rec.levelno > logging.INFO)
    _logger.addHandler(stderr_handler)