# voting/utils.py

import base64
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import datetime

def decode_qr_code_from_frame(frame_data):
    try:
        # Remove 'data:image/jpeg;base64,' prefix from frame data
        frame_data = frame_data.split(',')[1]

        # Decode the base64-encoded image
        img_bytes = base64.b64decode(frame_data)
        img_array = np.frombuffer(img_bytes, np.uint8)

        # Convert to OpenCV image format
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Process the image to detect QR codes
        qr_codes = decode(img)
        if qr_codes:
            for qr_code in qr_codes:
                qr_code_data = qr_code.data.decode('utf-8')
                print("Decoded QR Code:", qr_code_data)
                if is_valid_student_qr(qr_code_data):
                    return qr_code_data  # Return the decoded QR code data

    except Exception as e:
        print("Error decoding QR code:", e)

    return None  # If no valid QR code is found or error occurs

def is_valid_student_qr(qr_code_data):
    """Validate the student QR code format."""
    current_year = datetime.datetime.now().year % 100  # Get the last two digits of the current year
    if len(qr_code_data) == 7 and qr_code_data[:2].isdigit() and qr_code_data[2:4].isalpha() and qr_code_data[4:].isdigit():
        year = int(qr_code_data[:2])  # Extract the two-digit year
        if current_year - year in range(1, 4):  # Check if the year is within the valid range
            return True
    return False
