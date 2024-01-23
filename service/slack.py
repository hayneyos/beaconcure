import re
import sys
from io import BytesIO
import os
import requests
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from PIL import Image

# Extend the system path for specific Linux platforms to include custom directories
if sys.platform == "linux" or sys.platform == "linux2":
    sys.path.extend(['/home/yossih/'])
    sys.path.extend(['/home/yossih/beaconcure/'])
    sys.path.extend(['/home/yossih/beaconcure/service'])

# Importing encode/decode functions from the service package
from service.encoder_decoder import decode_image, encode_gif


# Define the SlackBot class
class SlackBot:
    _instance = None  # Singleton instance

    # Singleton pattern implementation
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SlackBot, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # Decipher the message from the text
    def decipher(self, text):
        try:
            parts = text.split(" ")
            if (len(parts) == 2):
                command, file_name = parts

                if (command == "Decipher"):
                    bot = SlackBot()
                    bot.handle_file_shared(file_name)
                    message = "message encrypted within the file " + file_name
        except Exception as exp:
            message = 'File not found / Parsing Error'

        return message

    # Encode the message into the image
    def encode(self, text):
        try:
            pattern = r'(\w+)\("([^"]+)",\s*[“"]([^”"]+)[”"]\)'
            match = re.match(pattern, text)

            if match:
                command, image_name, example_text = match.groups()

                destination, file = self.get_file(image_name)
                encode_gif(destination, example_text)
                message = text + "encoded into the file"

        except Exception as exp:
            message = 'File / command parsing error'

        return message

    # Initialize the SlackBot
    def __init__(self):
        # Set up paths and load environment variables based on the platform
        if sys.platform == "linux" or sys.platform == "linux2":
            self.server_destination = "images/slack_download/"
            self.env_location = "/home/yossih/beaconcure/.env"
        else:
            self.server_destination = "../images/slack_download/"
            self.env_location = "../.env"

        load_dotenv(self.env_location)
        self.client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    # Download a file from a Slack URL to a local destination
    def download_slack_file(self, url_private, destination):
        try:
            headers = {'Authorization': 'Bearer ' + os.environ['SLACK_BOT_TOKEN']}
            response = requests.get(url_private, headers=headers, stream=True)

            if response.status_code == 200:
                with open(destination, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except Exception as exp:
            print(str(exp))

    # Handle a shared file event from Slack
    def handle_file_shared(self, file_name):
        try:
            destination, file = self.get_file(file_name)

            if destination is not None:
                with Image.open(destination) as img:
                    for frame in range(0, 1):
                        img.seek(frame)
                        decoded_message = decode_image(img)
                        self.client.chat_postMessage(channel="test", text=f"Image processed/ decode message = {decoded_message}")

        except SlackApiError as e:
            print(f"Slack API Error: {e.response['error']}")

    # Retrieve a file from Slack based on its name
    def get_file(self, file_name):
        destination = None
        response = self.client.files_list()

        if response["ok"]:
            files = response["files"]

            for file in files:
                if file['name'] == file_name and file['filetype'] in ['gif', 'png']:
                    url = file['url_private']
                    destination = f"{self.server_destination}/{file['name']}"
                    self.download_slack_file(url, destination)
                    break
        else:
            print(f"Error: {response['error']}")
        return destination, file


# Create an instance of SlackBot and test its functionalities
bot = SlackBot()
text = """encode("giphy_color.gif", “This is an example text”)"""
bot.encode(text)

bot.handle_file_shared("giphy_color_encoded.png")
