import logging
from flask import Flask
from app.config import load_configurations, configure_logging
from app.views import webhook_blueprint
import app.services.genai_service as genai_service


app = Flask(__name__)

# Load configurations and logging settings
load_configurations(app)
configure_logging()
genai_service.configure_gen_ai_service()

# Import and register blueprints, if any
app.register_blueprint(webhook_blueprint)

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8001)
