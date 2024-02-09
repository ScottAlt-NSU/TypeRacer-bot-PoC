from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
current_typing_speed = typing_speed_element.get_attribute("title")  # Use "title" attribute to get the precise speed

try:
    # Convert to float and calculate 10% more
    current_typing_speed = float(current_typing_speed)
    adjusted_typing_speed = int(current_typing_speed * 3)  # Increase by 10% and convert to int for simplicity
except ValueError:
    # Fallback speed if there's an issue parsing the speed
    adjusted_typing_speed = 100  # Default or fallback typing speed

print(f"Original Typing Speed: {current_typing_speed} wpm, Adjusted Typing Speed: {adjusted_typing_speed} wpm")

# Initiating the race with Ctrl+Alt+I
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('I').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
actions.perform()  # Make sure to call perform() to execute the action chain

# Wait for the race to be ready. Adjust the time as needed or use WebDriverWait for specific elements
time.sleep(5)  # Increase this if necessary

# Now, find the element containing the text. Adjust the XPath if necessary
try:
    div_with_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@style, 'font-size: 20px; font-family: monospace;')]"))
    )
    text_to_type = div_with_text.text
    print("Extracted text to type:", text_to_type)

    input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'txtInput')))
    type_like_human(input_field, text_to_type, adjusted_typing_speed)
except Exception as e:
    print(f"Error encountered: {e}")


input("Press Enter to close the browser and exit the script...")

# Close the browser after user input
driver.quit()
