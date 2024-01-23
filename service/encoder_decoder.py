import imageio
from PIL import Image


# Convert a string message to its binary representation
def string_to_binary(message):
    return ''.join(format(ord(c), '08b') for c in message)


# Convert a binary string to ASCII text
def binary_to_string(binary):
    binary_values = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    ascii_characters = [chr(int(binary_value, 2)) for binary_value in binary_values]
    return ''.join(ascii_characters)


# Encode a message into an image
def encode_image(img, message):
    # Append a terminator sequence to the binary message
    binary_message = string_to_binary(message) + '1111111111111110'
    data_index = 0
    img = img.convert("RGBA")

    # Iterate over each pixel to embed the message
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img.getpixel((x, y)))
            c_pixel = pixel.copy()  # Copy of the current pixel for logging

            # Modify each RGB value of the pixel based on the message bits
            for n in range(0, 3):
                if data_index < len(binary_message):
                    binary_pos = int(binary_message[data_index])
                    pixel[n] = pixel[n] & ~1 | binary_pos
                    data_index += 1

            # Update the pixel with the new RGB values
            img.putpixel((x, y), tuple(pixel))

    # Return the modified image and a flag indicating if the message was fully encoded
    return img, data_index >= len(binary_message)


# Decode a message from a GIF using imageio library
def decode_by_imageio(output_gif_path):
    reader = imageio.get_reader(output_gif_path)
    for frame_number, frame in enumerate(reader):
        pil_image = Image.fromarray(frame)
        decoded_message = decode_image(pil_image)
        print(decoded_message)
        break  # Only decode the first frame


# Decode a message from a GIF using PIL
def decode_by_pil(encoded_file_name):
    with Image.open(encoded_file_name) as img:
        for frame in range(img.n_frames):
            img.seek(frame)
            decoded_message = decode_image(img)
            print(decoded_message)
            break  # Only decode the first frame


# Decode a message from an image
def decode_image(img):
    binary_message = ""
    img = img.convert("RGBA")

    # Extract the message from the RGB values of each pixel
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img.getpixel((x, y)))
            for n in range(0, 3):
                binary_message += str(pixel[n] & 1)

    # Split the binary message by the terminator and convert to ASCII
    binary_message = binary_message.split('1111111111111110')[0]
    message = binary_to_string(binary_message)
    return message


# Encode a message into a GIF
def encode_gif(input_gif_path, message, output_gif_path=""):
    with Image.open(input_gif_path) as img:
        frames = []
        message_encoded = False

        # Encode the message in the first frame only
        for frame in range(0, 1):
            img.seek(frame)
            if not message_encoded:
                encoded_frame, message_encoded = encode_image(img.copy(), message)
                frames.append(encoded_frame)
            else:
                frames.append(img.copy())

        # Set the default output path if not provided
        if (output_gif_path == ''):
            part1, separator, part2 = input_gif_path.rpartition('.')
            arr = [part1, part2]
            arr[0] = arr[0].replace("original", "encoded") + "_encoded"
            arr[1] = "png"
            output_gif_path = ".".join(arr)

        # Save the encoded GIF
        frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0)
        return output_gif_path
