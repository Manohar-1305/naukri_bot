import os
import logging
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Local resume path
DOWNLOAD_PATH = os.path.expanduser("~/Documents/Manohar_Pinnamshetty.pdf")

# Naukri Credentials
EMAIL = "manohar.shetty507@gmail.com"
PASSWORD = "Manohar@1305"

# Email Notification Config (Use app password if using Gmail)
SENDER_EMAIL = "tradingcontentdrive@gmail.com"
SENDER_PASSWORD = "abkt ynfw usog pgdx"
RECEIVER_EMAIL = "manohar.shetty507@gmail.com"

def send_email_notification():
    """Send an email notification after successful resume upload."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "✅ Naukri Resume Upload Successful"

    body = "Hi Manohar,\n\nYour resume has been successfully uploaded to Naukri.com.\n\nBest,\nAutomation Bot 🤖"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        logger.info("📧 Email notification sent successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")

def upload_resume_naukri():
    """Automate Naukri.com resume upload."""
    logger.info("Launching browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    try:
        logger.info("Opening Naukri.com...")
        driver.get("https://www.naukri.com/")

        # Handle popups (if any)
        try:
            popup_close = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Later')]")))
            popup_close.click()
            logger.info("Closed popup.")
        except:
            logger.info("ℹ️ No popup found, continuing...")

        # Click Login
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Login']")))
        login_button.click()
        logger.info("Clicked Login...")

        # Enter Email
        email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")))
        email_field.click()
        email_field.send_keys(EMAIL)
        logger.info("Entered Email...")

        # Enter Password
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_field.send_keys(PASSWORD)

        # Click Login Button
        login_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
        login_submit.click()

        time.sleep(5)
        logger.info("✅ Login successful!")

        # Navigate to Profile and Upload Resume
        driver.get("https://www.naukri.com/mnjuser/profile")
        upload_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        upload_btn.send_keys(DOWNLOAD_PATH)

        time.sleep(10)
        logger.info("✅ Resume uploaded successfully!")

        # Send email notification
        send_email_notification()

    except Exception as e:
        logger.error(f"❌ Error during resume upload: {e}")

    finally:
        driver.quit()
        logger.info("✅ Process completed successfully!")

if __name__ == "__main__":
    logger.info("Starting Resume Update Process...")
    upload_resume_naukri()
