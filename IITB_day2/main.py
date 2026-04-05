import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ---------- SETTINGS ----------
IMAGES_PER_LABEL = 5
BASE_DIR = os.getcwd()
IMAGES_DIR = os.path.join(BASE_DIR, "images")
LABELS_FILE = "label.txt"

# Create images folder if it doesn't exist
os.makedirs(IMAGES_DIR, exist_ok=True)

# ---------- SELENIUM SETUP ----------
driver = webdriver.Chrome()
driver.maximize_window()

# ---------- READ LABELS ----------
with open(LABELS_FILE, "r") as file:
    labels = [line.strip() for line in file if line.strip()]

# ---------- FUNCTION TO DOWNLOAD IMAGES ----------
def download_images(keyword):
    # Open Google Images
    search_url = f"https://www.google.com/search?q={keyword}&tbm=isch"
    driver.get(search_url)
    time.sleep(3)

    # Scroll down to load more images
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 1000)")
        time.sleep(2)

    # Find image elements
    images = driver.find_elements(By.CSS_SELECTOR, "img")

    # Create folder for this keyword
    save_folder = os.path.join(IMAGES_DIR, keyword.replace(" ", "_"))
    os.makedirs(save_folder, exist_ok=True)

    count = 0
    for img in images:
        if count >= IMAGES_PER_LABEL:
            break
        src = img.get_attribute("src")
        if src and src.startswith("http"):
            try:
                img_data = requests.get(src, timeout=5).content
                with open(os.path.join(save_folder, f"{count}.jpg"), "wb") as f:
                    f.write(img_data)
                count += 1
            except:
                continue

    print(f"✅ Downloaded {count} images for '{keyword}'")

# ---------- MAIN LOOP ----------
for label in labels:
    download_images(label)

driver.quit()
print("🎉 All images downloaded!")
