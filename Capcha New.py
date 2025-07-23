from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from google.cloud import vision
import io
import os
import time
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# import pytesseract

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Your Token"


# Optional: Run Chrome in headless mode
options = Options()
# options.add_argument("--headless")  # Uncomment to run without GUI

# Launch browser
driver = webdriver.Chrome(service=Service(), options=options)
driver.get("Any website u want")
time.sleep(5)  # Let the page load

try:
    # Wait for a visible element with 'Close' text
    wait = WebDriverWait(driver, 10)
    close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Close']")))
    close_btn.click()
    print("Popup closed successfully.")
except Exception as e:
    print("Popup not found or already closed.", e)

# Keep browser open a bit for observation
time.sleep(2)


# Locate the CAPTCHA image
captcha_element = driver.find_element(By.ID, "imgCaptcha")  # Adjust ID if different

# Save the CAPTCHA image
captcha_element.screenshot("captcha.png")
captcha_img = Image.open("captcha.png")
# Load the image
image= Image.open("captcha.png")
image.show()
# text = pytesseract.image_to_string(captcha_img)


def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        print("Extracted Text:", texts[0].description.strip())
        return texts[0].description.strip()
    else:
        print("No text detected.")
        return ""

# Example usage
captcha_text = detect_text("captcha.png")

captcha_input = driver.find_element(By.ID, "txtImg") 
captcha_input.clear()
captcha_input.send_keys(captcha_text)


   