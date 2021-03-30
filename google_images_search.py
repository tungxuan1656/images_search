import requests
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
from fake_useragent import UserAgent
from urllib.parse import unquote
from tqdm import tqdm
import argparse


def save_image(url, save_dir):
    # Get the file name and type
    file_name = os.path.basename(url).replace('?', '_')
    type = file_name.split(".")[-1]
    if type.lower() not in ["jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
        file_name += '.jpg'
        return
    file_name = time.strftime("%Y%m%d_%H%M%S_") + file_name
    try:
        save_path = os.path.join(save_dir, file_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        ua = UserAgent(verify_ssl=False)
        headers = {"User-Agent": ua.random}
        r = requests.get(url, stream=True, headers=headers, timeout=20)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            return "[!] Image returned a {} error at {}.".format(r.status_code, url)
    except Exception as e:
        return "[!] Error {} at {}".format(e, url)


def search(query, max_results=35):
    # Create a browser and resize depending on user preference
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.headless = True
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    browser = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
    browser.set_window_size(1024, 768)

    print("[%] Successfully launched ChromeDriver")

    url = f'https://www.google.com/search?q={query}&source=lnms&tbm=isch'
    # Open the link
    print('[%] URL Search:', url)

    browser.get(url)
    time.sleep(1)
    print("[%] Successfully opened link.")

    count_scroll = 0
    if max_results >= 50 and max_results <= 100:
        count_scroll = 5
    if max_results > 100 and max_results <= 200:
        count_scroll = 10
    if max_results > 200:
        count_scroll = 30

    # Scroll down
    element = browser.find_element_by_tag_name("body")
    print("[%] Scrolling down.")
    for i in range(count_scroll):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)  # bot id protection

    if count_scroll > 400:
        try:
            browser.find_element_by_id("smb").click()
            print("[%] Successfully clicked 'Show More Button'.")
            for i in range(50):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)  # bot id protection
        except Exception:
            for i in range(10):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)  # bot id protection

    hrefs = []
    try:
        elements = browser.find_elements_by_css_selector('a.wXeWr.islib.nfEiy.mM5pbd')
        print(f'[%] Found {len(elements)} images. Get origin url of {max_results} images:')
        for e in tqdm(elements[:max_results], leave=False):
            e.click()
            time.sleep(0.5)
            href = e.get_attribute('href')
            if href is not None:
                hrefs.append(href)
    except Exception as e:
        print(e)

    # browser.save_screenshot('screenshot.png')
    # # Get page source and close the browser
    # source = browser.page_source
    # with open('{}/dataset/logs/google/source.html'.format(os.getcwd()), 'w+', encoding='utf-8', errors='replace') as f:
    #     f.write(source)

    time.sleep(1)
    browser.close()
    print("[%] Closed ChromeDriver.")

    image_urls = []
    for href in hrefs:
        s = href.split('&')
        if len(s) > 0:
            uri_encoded = s[0][s[0].index('imgurl='):][7:]
            image_urls.append(unquote(uri_encoded))
    return image_urls


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Scrape images from the internet.")
    parser.add_argument(
        "query", help="Query that should be used to scrape images.", type=str)
    parser.add_argument(
        "--save_dir", help="Folder save images. If default, save to folder data/google/{query}", default='./data/google', type=str, required=False)
    parser.add_argument(
        "--max_results", help="Amount of images to be scraped.", default=35, required=False, type=int)

    args = parser.parse_args()

    query = args.query
    save_dir = args.save_dir
    if save_dir == './data/google':
        save_dir = f'./data/google/{query}'
    max_results = int(args.max_results)

    image_urls = search(query, max_results=max_results)
    print("\n[%] Save Image")
    arr_errors = []
    for url in tqdm(image_urls):
        e_desc = save_image(url, save_dir)
        if e_desc != None:
            arr_errors.append(e_desc)
    if len(arr_errors) != 0:
        print("\n[!] Error:")
        for e in arr_errors:
            print(e)
    print("[%] Done. Please visit folder", save_dir)
