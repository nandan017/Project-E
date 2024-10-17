# voting/utils.py

import base64
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import datetime
from io import BytesIO
from PIL import Image


def decode_qr_code_from_frame(base64_image):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(base64_image)

        # Create a PIL Image object from the bytes
        image = Image.open(BytesIO(image_data))

        # Use pyzbar to decode the QR code from the image
        decoded_objects = decode(image)

        if decoded_objects:
            qr_code_data = decoded_objects[0].data.decode('utf-8')
            return qr_code_data
        else:
            print("No QR code found.")
            return None
    except Exception as e:
        print("Error during QR code decoding:", e)
        return None

def is_valid_student_qr(qr_code_data):
    """Validate the student QR code format."""
    current_year = datetime.datetime.now().year % 100  # Get the last two digits of the current year
    if len(qr_code_data) == 7 and qr_code_data[:2].isdigit() and qr_code_data[2:4].isalnum() and qr_code_data[4:].isdigit():
        year = int(qr_code_data[:2])  # Extract the two-digit year
        if current_year - year in range(0, 4):  # Check if the year is within the valid range
            return True
    return False
