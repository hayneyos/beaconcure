import logging
import os
import re
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from service.encoder_decoder import encode_gif
from service.slack import SlackBot
from slackeventsapi import SlackEventAdapter

# Load environment variables from .env file
env_path = ".env"
load_dotenv(env_path)

# Initialize Flask application
app = Flask(__name__)

# Set up Slack event adapter for handling Slack events
slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], '/slack/events', app)

# Configure logging
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
log_file = f"flask_log.log"
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
handler.setFormatter(formatter)

# Set log level to DEBUG for detailed logging
app.logger.setLevel(logging.DEBUG)
# Add the log handler to the Flask app
app.logger.addHandler(handler)


# Decorator for handling "message" event from Slack
@slack_event_adapter.on("message")
def message(payload):
    # Log the payload for debugging purposes
    app.logger.debug(f'new request -> "message", {str(payload)}')

    # Extracting details from the payload
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    print(f"{channel_id} {user_id} {text}")

    # Initialize SlackBot
    bot = SlackBot()

    message = ""
    # Decipher or encode text based on the command
    if (text.strip().find("Decipher") >= 0):
        message = bot.decipher(text)

    elif (text.strip().find("encode") >= 0):
        message = bot.encode(text)

    # Respond with the processed message
    return jsonify({'status': 'OK', 'message': message}), 200


# Route for the home page
@app.route('/', methods=['GET'])
def home():
    app.logger.debug(f'new request -> "/"')
    return jsonify({'status': 'OK'}), 200


# Route for testing
@app.route('/test', methods=['GET'])
def test():
    app.logger.debug(f'new request -> "/test"')
    bot = SlackBot()
    bot.client.chat_postMessage(channel="test", text="Check2")
    return jsonify({'status': 'OK'}), 200


# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8012)
