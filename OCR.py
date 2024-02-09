from PIL import Image, ImageFilter, ImageEnhance
import requests
from io import BytesIO
import pytesseract
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from openai import OpenAI
import easyocr
import os
import requests
from spellchecker import SpellChecker

reader = easyocr.Reader(['en'], gpu=False)  # this needs to run only once to load the model into memory

def download_file(url, filename=None):
    """Download a file from a given URL and save it to the script's directory."""
    # If no filename is given, use the last part of the URL
    if filename is None:
        filename = url.split('/')[-1]

    # Get the response from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the download was successful

    # Define the path to save the file (in the current script's directory)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, filename)

    # Write the file to the specified path
    with open(file_path, 'wb') as file:
        file.write(response.content)

    print(f"File downloaded and saved as {file_path}")

# URL from which file will be downloaded
url = 'https://play.typeracer.com/challenge?id=1707500092214tr:grandma_suzan'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Assuming the content you are downloading is a text file, or similar.
    # You might need to adjust the code for other types of files (e.g., binary data)
    content = response.content

    # Define the local filename to save the downloaded file
    filename = 'image1.jpeg'  # Adjust the file extension based on the content type

    # Open file in binary write mode and save the content
    with open(filename, 'wb') as file:
        file.write(content)

    print(f'File downloaded successfully and saved as {filename}')
else:
    print('Failed to download the file. Status code:', response.status_code)

file_path = download_file('https://play.typeracer.com/challenge?id=1707500092214tr:grandma_suzan')
image_path = 'challenge-3.jpeg'

result = reader.readtext(image_path, detail=0)

print(result)

# OCR output
ocr_output = result

# Concatenate text segments into a single string
raw_text = ' '.join(ocr_output)

# Basic sanitization (example: correcting 'l' to 'I', '0' to 'o', etc.)
# This step can be expanded based on common OCR mistakes observed in your outputs
# sanitized_text = raw_text.replace('l', 'I').replace('0', 'o').replace('4', 'A').replace('Idown', 'down')

print(raw_text)
