import os
import logging
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Automate resume upload
def upload_resume(email, password, resume_path):
    logger.info("Launching browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    try:
        logger.info("Opening Naukri.com...")
        driver.get("https://www.naukri.com/")

        # Handle popup
        try:
            popup_close = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Later')]")))
            popup_close.click()
            logger.info("Closed popup.")
        except:
            logger.info("No popup found, continuing...")

        # Login
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Login']")))
        login_button.click()

        email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")))
        email_field.send_keys(email)

        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_field.send_keys(password)

        login_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
        login_submit.click()

        time.sleep(5)
        logger.info("Login successful!")

        # Navigate to profile
        driver.get("https://www.naukri.com/mnjuser/profile")
        upload_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        upload_btn.send_keys(resume_path)

        time.sleep(10)
        logger.info("Resume uploaded successfully!")
        messagebox.showinfo("Success", "Resume uploaded successfully!")

    except Exception as e:
        logger.error(f"Error: {e}")
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
    finally:
        driver.quit()

# GUI using Tkinter
class ResumeUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Naukri Resume Uploader")
        self.root.geometry("400x300")

        # Email Entry
        tk.Label(root, text="Email").pack(pady=(10, 0))
        self.email_entry = tk.Entry(root, width=40)
        self.email_entry.pack()

        # Password Entry
        tk.Label(root, text="Password").pack(pady=(10, 0))
        self.password_entry = tk.Entry(root, show="*", width=40)
        self.password_entry.pack()

        # Resume File Selection
        tk.Label(root, text="Resume File").pack(pady=(10, 0))
        self.resume_path_var = tk.StringVar()
        self.resume_entry = tk.Entry(root, textvariable=self.resume_path_var, width=30)
        self.resume_entry.pack(side="left", padx=(10, 0), pady=(0, 10))
        tk.Button(root, text="Browse", command=self.browse_file).pack(side="left", padx=5)

        # Submit Button
        tk.Button(root, text="Upload Resume", command=self.submit).pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.resume_path_var.set(file_path)

    def submit(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        resume_path = self.resume_path_var.get()

        if not email or not password or not resume_path:
            messagebox.showwarning("Input Error", "Please fill in all fields and select a resume.")
            return

        upload_resume(email, password, resume_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeUploaderApp(root)
    root.mainloop()
