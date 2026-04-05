import os
import requests
import time
import hashlib
import base64
from urllib.parse import urlparse
import tempfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


def load_labels(labels_file):
    with open(labels_file, 'r') as f:
        labels = [line.strip() for line in f if line.strip()]
    return labels


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    temp_dir = tempfile.mkdtemp(prefix='selenium_')
    options.add_argument(f'--user-data-dir={temp_dir}')

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def download_image(img_url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com/'}
        response = requests.get(img_url, headers=headers, timeout=15, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except:
        return False


def save_base64_image(base64_string, save_path):
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        img_data = base64.b64decode(base64_string)
        with open(save_path, 'wb') as f:
            f.write(img_data)
        return True
    except:
        return False


def extract_images_from_google(driver, search_query, output_dir, max_images=250):
    print(f"\n{'='*60}")
    print(f"Searching for: {search_query}")
    print(f"{'='*60}")

    try:
        driver.get(f"https://www.google.com/search?q={search_query}&tbm=isch")
        time.sleep(3)

        wait = WebDriverWait(driver, 10)

        # Remove size filter to get all medium + large images
        print("No size filter applied downloading all medium and large images")

        thumbnails = []
        last_height = 0
        while len(thumbnails) < max_images:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            all_imgs = driver.find_elements(By.CSS_SELECTOR, 'img.YQ4gaf')
            thumbnails = [img for img in all_imgs if img.size['width'] > 50 and img.size['height'] > 50]
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print(f"Found {len(thumbnails)} thumbnails")

        downloaded = 0
        actions = ActionChains(driver)

        for i, thumb in enumerate(thumbnails[:max_images]):
            if downloaded >= max_images:
                break

            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", thumb)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", thumb)
                time.sleep(3)

                preview_img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c, img.iPVvYb, img.n3VNCb")))

                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return arguments[0].naturalWidth > 0;", preview_img)
                )

                w = driver.execute_script("return arguments[0].naturalWidth;", preview_img)
                h = driver.execute_script("return arguments[0].naturalHeight;", preview_img)

                # Removed low-res skip – download all medium and large
                print(f"Processing {i+1}: {w}x{h}")

                src = preview_img.get_attribute('src')
                if not src:
                    raise ValueError("No src attribute")

                ext = '.jpg' if src.startswith('data:') else (os.path.splitext(urlparse(src).path)[1] or '.jpg')
                hash_part = hashlib.md5(src.encode()).hexdigest()[:8]
                filename = f"{search_query.replace(' ', '_')}_{i+1:03d}_{hash_part}{ext}"
                path = os.path.join(output_dir, filename)

                success = save_base64_image(src, path) if src.startswith('data:') else download_image(src, path)

                if success:
                    downloaded += 1
                    print(f"Downloaded {downloaded}: {w}x{h}")
                else:
                    print(f"Download failed {i+1}")

                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(1)

            except Exception as e:
                print(f"Error on {i+1}: {e}")
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(1)
                continue

        print(f"Completed {search_query}: {downloaded} images")
        return downloaded

    except Exception as e:
        print(f"Error: {e}")
        return 0


def main():
    labels_file = os.path.join(os.getcwd(), "label.txt")
    output_dir = os.path.join(os.getcwd(), "images")
    images_per_label = 10

    if not os.path.exists(labels_file):
        print("Labels file not found")
        return

    labels = load_labels(labels_file)
    os.makedirs(output_dir, exist_ok=True)

    driver = setup_driver()

    try:
        total = 0
        for i, label in enumerate(labels, 1):
            print(f"\n[Label {i}/{len(labels)}]")
            label_dir = os.path.join(output_dir, label.replace(" ", "_"))
            os.makedirs(label_dir, exist_ok=True)
            count = extract_images_from_google(driver, label, label_dir, images_per_label)
            total += count
            time.sleep(5)

        print(f"\nTotal downloaded: {total}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()