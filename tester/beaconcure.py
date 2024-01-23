import cap as cap
import cv2
import imageio as imageio
from PIL import Image
# import cv2
import binascii

from service.encoder_decoder import encode_gif, decode_image, decode_by_pil, decode_by_imageio


def extract_frames(gif_path):
    with Image.open(gif_path) as img:
        # Check if the image is a GIF
        if not img.is_animated:
            raise ValueError("The image is not an animated GIF")

        # Extract each frame
        frames = []
        counter = 1
        for frame in range(img.n_frames):
            img.seek(frame)
            frames.append(img.copy())
        return frames


def save_frames(frames, all_message):
    # tokens = tokenize(all_message)
    # char_chunks = split_into_char_chunks(tokens, 10)  # Specify the chunk size

    # You can then process these frames as needed
    len(frames)
    for i, frame in enumerate(frames):
        frame.save(f"frame_{i}.png")


def merge_list_of_png_to_gif(encoded_file, decode_file_name):
    other_frames = extract_frames(decode_file_name)
    png_files = [encoded_file]  # Replace with your file paths

    # Open images and store in a list
    images = [Image.open(file) for file in png_files]
    images.extend(other_frames)

    # Create the GIF
    output_gif_path = 'images/encoded/encoded_file_gif.gif'  # Name of the output GIF file
    images[0].save(output_gif_path, save_all=True, append_images=images[1:], optimize=False)

    print(f"GIF created successfully: {output_gif_path}")
    return output_gif_path


# org_file_name = 'images/original/Rotating_earth.gif'
# org_file_name = 'images/original/giphy.gif'
# org_file_name = 'images/original/giphy_color.gif'
# org_file_name = 'images/original/arbel.jpg'
# org_file_name = 'images/original/Screenshot_20200220-105728.png'
org_file_name = '../images/original/330px-White_House_Tumblr_launch_image.jpg'

encoded_file = org_file_name
output_gif_path = encode_gif(org_file_name, 'Your secret message aaaa')

decode_by_pil(output_gif_path)
decode_by_imageio(output_gif_path)
