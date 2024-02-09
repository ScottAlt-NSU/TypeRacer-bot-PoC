

from selenium import webdriver
from PIL import Image
import pytesseract
import requests
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

# Initialize Selenium WebDriver

# Locate the image (assuming you can directly get its URL)
# Find the image element
# Adjust the selector as needed to find the image with src that starts with 'challenge?id='
image_element = driver.find_element_by_xpath("//img[contains(@src, 'challenge?id=')]")
image_url = image_element.get_attribute('src')


# Download the image using requests
def perform_ocr_old(image_url):
    # Download the image using requests
    response = requests.get(image_url)
    if response.status_code == 200:
        # Convert the image content directly to an Image object without saving it
        image = Image.open(BytesIO(response.content))
        # Use pytesseract to perform OCR on the image
        text = pytesseract.image_to_string(image)
        print(text)
        return text
    else:
        raise Exception("Failed to download the image.")
