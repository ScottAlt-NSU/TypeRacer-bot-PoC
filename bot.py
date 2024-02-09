import os
import re
import time
from datetime import datetime
from io import BytesIO

import easyocr
import openai
import pytesseract
import requests
from PIL import Image
from fuzzywuzzy import process
from nltk.corpus import words
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from textblob import TextBlob

username = "Grandma_Suzan"
password = "Grandma_Suzan"

reader = easyocr.Reader(['en'], gpu=False)


def initialize_driver():
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to msedgedriver
    path_to_webdriver = os.path.join(current_script_dir, 'msedgedriver')

    # Initialize the service with the path to msedgedriver
    webdriver_service = Service(executable_path=path_to_webdriver)
    driver = webdriver.Edge(service=webdriver_service)
    return driver


def extract_similar_length_text_from_words(ocr_text, transcript_path):
    # Open and read the transcript file
    with open(transcript_path, 'r', encoding='utf-8') as file:
        transcript = file.read()

    # Extract the first two words from the OCR text
    first_three_words = ' '.join(ocr_text.split()[:3])

    # Search for the first occurrence of these words in the transcript
    start_index = transcript.find(first_three_words)

    if start_index != -1:
        # Calculate the end index based on the length of the OCR text
        end_index = start_index + len(ocr_text)

        # Extract the corresponding text from the transcript
        extracted_text = transcript[start_index:end_index]

        return extracted_text
    else:
        # Return None or an appropriate response if the substring is not found
        return None

def find_best_match_in_transcript(ocr_text, transcript_path):
    """
    Finds the best match for the OCR text in the transcript and returns the matching transcript text.

    :param ocr_text: The text extracted from OCR.
    :param transcript_path: Path to the transcript file.
    :return: Best matching sentence from the transcript.
    """
    # Load the transcript
    with open(transcript_path, 'r', encoding='utf-8') as file:
        transcript = file.read()

    # Split the transcript into sentences
    sentences = transcript.split(
        '.')  # This is a simple split, you might need a more sophisticated sentence tokenizer for complex texts

    # Find the best match for the OCR text in the transcript sentences
    best_match, score = process.extractOne(ocr_text, sentences)

    # Return the best matching sentence
    return best_match.strip()


def get_current_timestamp_ms():
    """
    Returns the current UTC time as a Unix timestamp in milliseconds.
    """
    now = datetime.utcnow()
    timestamp_ms = int(now.timestamp() * 1000)
    return timestamp_ms


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

        # Preprocess the image
        # Convert to grayscale
        image = image.convert('L')
        # Apply thresholding
        threshold = 200
        image = image.point(lambda p: p > threshold and 255)

        # Use pytesseract to perform OCR on the image
        # Specify language if known, e.g., 'eng' for English
        # Use a custom configuration, e.g., --psm 6 assumes a single uniform block of text
        text = pytesseract.image_to_string(image, lang='eng')

        print(f"original OCR: {text}")
        # Replace new lines and carriage returns with a space
        text = text.replace('\n', ' ').replace('\r', ' ')
        # Reduce all multiple spaces to a single space
        text = re.sub(' +', ' ', text)

        print(f"slightly sanitized {text}")
        return text
    else:
        raise Exception("Failed to download the image.")


def process_image_and_query_ai(image_url):
    """
    Performs OCR on the given image URL, queries an AI model for a speculative guess of the OCR text,
    and returns the AI-sanitized text.
    """
    # Perform OCR to extract text from the image
    ocr_text = perform_ocr_text(image_url)  # Ensure this function is correctly defined and imported
    print("OCR Text:", ocr_text)

    # Construct the prompt for the AI
    prompt_text = f"Tell me only the ANSWER, no background info - take a speculative guess at what this ocr text is meant to say. Output as markdown so I can easily copy and paste it: {ocr_text}"

    # Initialize the OpenAI client with your API key
    openai.api_key = 'your_openai_api_key_here'

    # Query the OpenAI API
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt_text,
            }
        ],
    )

    # Extracting the response
    answer = chat_completion.choices[0].message.content
    print(f"Post AI sanitization: {answer}")

    return answer


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

        if adjusted_typing_speed == 0:
            adjusted_typing_speed = 300

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

        input_field = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, 'txtInput')))
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
        # input("Captcha required, press Enter to continue...")
        begin_test_button.click()
        timestamp = get_current_timestamp_ms()

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
            timestamp_image_url = f"https://play.typeracer.com/challenge?id={timestamp}+tr:Grandma_Suzan"
            print("Timestamped Image URL:", timestamp_image_url)
            print("Constructed Image URL:", image_url)

            file_path = 'list_of_challenges.txt'
            # Open the file in append mode and write the image_url to it
            with open(file_path, 'a') as file:
                file.write(image_url + '\n')  # Append the URL and a newline character to the file

        except TimeoutException:
            print("Failed to find the image within the timeout period.")

        try:
            # if you want to try with AI
            # ai_sanitized_text = process_image_and_query_ai(image_url)
            # print(ai_sanitized_text)
            # sanitized_text = perform_ocr_text(image_url)

            response = requests.get(image_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Assuming the content you are downloading is a text file, or similar.
                # You might need to adjust the code for other types of files (e.g., binary data)
                content = response.content

                # Define the local filename to save the downloaded file
                directory = 'images/training'

                timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')

                filename = 'image1.jpeg'  # Adjust the file extension based on the content type
                filename2 = f'image_{timestamp}.jpeg'
                file_path = os.path.join(directory, filename2)

                with open(file_path, 'wb') as file:
                    file.write(content)

                # Open file in binary write mode and save the content
                with open(filename, 'wb') as file:
                    file.write(content)

                print(f'File downloaded successfully and saved as {filename}')
            else:
                print('Failed to download the file. Status code:', response.status_code)

            file_path = download_file(image_url)
            image_path = "image1.jpeg"

            result = reader.readtext(image_path, detail=0)

            print(f"initial output: {result}")

            # OCR output
            ocr_output = result

            # Concatenate text segments into a single string
            raw_text = ' '.join(ocr_output)
            print(f"cleaned output: {raw_text}")

            cleaned_text = re.sub(r'[~()_{}\[\]|\\/]', '', raw_text)

            print(f"cleaned output V2: {cleaned_text}")

            words = cleaned_text.split()

            corrected_words = []
            for word in words:
                corrected_word = TextBlob(word)
                # Using the corrected spelling of the word
                corrected_words.append(str(corrected_word.correct()))

            # Joining the corrected words back into a full sentence
            corrected_text = ' '.join(corrected_words)

            print(f"Autocorrected output: {corrected_text}")

            transcript_file = "alice.txt"

            extracted_text = extract_similar_length_text_from_words(corrected_text, transcript_file)

            if extracted_text:
                print(f"Extracted text from transcript: {extracted_text}")
                input_field_ocr = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'challengeTextArea')))
                type_like_human(input_field_ocr, extracted_text, adjusted_typing_speed)
            else:
                print("The first three words of the OCR text were not found in the transcript.")

                input_field_ocr = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'challengeTextArea')))
                type_like_human(input_field_ocr, corrected_text, adjusted_typing_speed)

        except:

            input("Press Enter to close the browser and exit the script...")

    finally:

            input("Press Enter to close the browser and exit the script...")

if __name__ == "__main__":
    main()
