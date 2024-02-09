from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def initialize_driver():
    webdriver_service = Service(
        r'C:\Users\sa2576\OneDrive - Nova Southeastern University\Documents\SNOW_Automation\SNOW_Automate\msedgedriver.exe')
    driver = webdriver.Edge(service=webdriver_service)
    return driver

def type_like_human(element, text, wpm=100):
    char_per_minute = wpm * 5
    delay = 60 / char_per_minute
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

driver = initialize_driver()
driver.get("https://play.typeracer.com/")
time.sleep(5)  # Initial wait for the page to load

# Initiating the race with Ctrl+Alt+I
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('I').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
actions.perform()  # Make sure to call perform() to execute the action chain

# Wait for the race to be ready. Adjust the time as needed or use WebDriverWait for specific elements
time.sleep(10)  # Increase this if necessary

# Now, find the element containing the text. Adjust the XPath if necessary
try:
    div_with_text = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@style, 'font-size: 20px; font-family: monospace;')]"))
    )
    text_to_type = div_with_text.text
    print("Extracted text to type:", text_to_type)

    input_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'txtInput')))
    type_like_human(input_field, text_to_type, 100)
except Exception as e:
    print(f"Error encountered: {e}")


input("Press Enter to close the browser and exit the script...")

# Close the browser after user input
driver.quit()
