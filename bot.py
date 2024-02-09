from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import requests
from io import BytesIO

import time
import os

username = "Grandma_Susan"
password = "Grandma_Susan"


def initialize_driver():
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to msedgedriver
    path_to_webdriver = os.path.join(current_script_dir, 'msedgedriver')

    # Initialize the service with the path to msedgedriver
    webdriver_service = Service(executable_path=path_to_webdriver)
    driver = webdriver.Edge(service=webdriver_service)
    return driver


def type_like_human(element, text, wpm=100):
    char_per_minute = wpm * 7

    delay = 60 / char_per_minute
    for char in text:
        element.send_keys(char)
        time.sleep(delay)


def perform_ocr_text(image_url):
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


def main():
    global image_url
    driver = initialize_driver()
    # Your existing code to navigate and interact with the web page
    driver = initialize_driver()
    driver.get("https://play.typeracer.com/")
    time.sleep(3)  # Initial wait for the page to load

    sign_in_link = driver.find_element(By.CLASS_NAME, "signIn")
    sign_in_link.click()

    time.sleep(2)

    # Locate and click the "Sign In" link
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "signIn"))).click()

    # Wait for the sign-in modal to appear
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "gwt-TextBox")))

    # Input the username
    username_field = driver.find_element(By.CLASS_NAME, "gwt-TextBox")
    username_field.send_keys(username)

    # Input the password
    password_field = driver.find_element(By.CLASS_NAME, "gwt-PasswordTextBox")
    password_field.send_keys(password)

    # Click the "Sign In" button
    sign_in_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
    sign_in_button.click()

    time.sleep(2)
    # Wait for the popup to be visible
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "xButton"))
    )

    # Locate and click the "close this popup" button
    close_popup_button = driver.find_element(By.CLASS_NAME, "xButton")
    close_popup_button.click()

    time.sleep(5)

    typing_speed_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "lblWpm"))
    )

    # Retrieve the current typing speed
    current_typing_speed_str = typing_speed_element.get_attribute("title").replace(" wpm", "")
    try:
        # Convert to float and calculate 10% more
        current_typing_speed = float(current_typing_speed_str)
        adjusted_typing_speed = int(current_typing_speed * 1.13)  # Increase by 12%
    except ValueError:
        # Fallback speed if there's an issue parsing the speed
        adjusted_typing_speed = 100  # Default or fallback typing speed

    print(f"Original Typing Speed: {current_typing_speed_str} wpm, Adjusted Typing Speed: {adjusted_typing_speed} wpm")

    # Initiating the race with Ctrl+Alt+I
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('I').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    actions.perform()  # Make sure to call perform() to execute the action chain

    # Wait for the race to be ready. Adjust the time as needed or use WebDriverWait for specific elements
    time.sleep(5)  # Increase this if necessary

    # Now, find the element containing the text. Adjust the XPath if necessary
    try:
        div_with_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@style, 'font-size: 20px; font-family: monospace;')]"))
        )
        text_to_type = div_with_text.text
        print("Extracted text to type:", text_to_type)

        input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'txtInput')))
        type_like_human(input_field, text_to_type, adjusted_typing_speed)
    except Exception as e:
        print(f"Error encountered: {e}")

    try:
        # Wait for the "Begin Test" button to appear within 5 seconds
        begin_test_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'gwt-Button') and contains(text(), 'Begin Test')]"))
        )
        # If the button is found, click it or continue with the script
        time.sleep(5)
        begin_test_button.click()
        print("Begin Test button found and clicked.")
        # Assuming you reach the point where you need to call OCR
        # Locate the image
        time.sleep(1)

        try:
            image_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "challengeImg"))
            )
            src_attribute = image_element.get_attribute('src')
            # print("Image SRC attribute:", src_attribute)
            # input("Captcha required, press Enter to continue...")

            # src_attribute = image_element.get_attribute('src')
            challenge_id = src_attribute.split('=')[1]  # Assuming 'src' format is 'challenge?id=XYZ'
            image_url = f"https://play.typeracer.com/challenge?id={challenge_id}"
            print("Constructed Image URL:", image_url)
        except TimeoutException:
            print("Failed to find the image within the timeout period.")

        try:
            ocr_text = perform_ocr_text(image_url)  # Ensure this function is correctly defined and imported
            print("OCR Text:", ocr_text)
            # Now use this text to type out using the predetermined speed logic
            input("Captcha required, press Enter to continue...")
            input_field_ocr = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'txtInput')))
            type_like_human(input_field_ocr, ocr_text, adjusted_typing_speed)

        except Exception as e:
            print(f"Error encountered: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    except Exception as e:
        input("Press Enter to close the browser and exit the script...")
        driver.quit()


if __name__ == "__main__":
    main()
