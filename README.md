# Slack Bot for Image Encoding and Decoding

## Project Overview

This project involves the development of a Slack bot capable of encoding and decoding messages within images. The bot integrates with Slack, allowing users to interact with it through Slack messages. It handles specific commands to encode text into images and decode text from images, making it a useful tool for secure communication.

## Features

- **Encode Messages**: The bot can encode text messages into images (GIFs or PNGs) shared in Slack.
- **Decode Messages**: It can also decode messages hidden in images and reply with the extracted text.
- **File Handling**: The bot manages file downloads from Slack and processes them to encode or decode messages.
- **Slack Integration**: Fully integrated with Slack, the bot can receive and send messages, as well as handle shared files in Slack channels.

## How It Works

- **Encoding**: When a user shares an image and sends an encoding command, the bot downloads the image, encodes the specified message into it, and re-uploads the modified image to Slack.
- **Decoding**: For decoding, when a user shares an image with an encoded message, the bot downloads it, extracts the hidden message, and replies with the decoded text in the Slack channel.

## Setup and Configuration

- The bot requires Python 3.x and several dependencies including `PIL`, `slack_sdk`, and `requests`.
- Environmental variables (like the Slack bot token) should be set in a `.env` file.
- Paths and configurations are set based on the operating system (Linux or others).

## Usage

- The bot listens to specific commands in Slack messages to perform encoding or decoding.
- For encoding, use the command format: `encode("image_file_name", “Your message here”)`.
- For decoding, simply share an image with an encoded message in a Slack channel where the bot is present.

## Limitations

- The current implementation encodes and decodes messages in the first frame of GIFs only. ( Release the first frame from it and save it as a png)
- It is designed to handle specific image formats (GIF and PNG).

## Future Enhancements

- Support for multiple frames in GIFs for encoding and decoding.
- Enhanced error handling and user feedback for better interaction.

## Author

Developed by Yossi Heine.

---

This project showcases the integration of image processing techniques with Slack APIs to create a functional and interactive bot for secure communication.
