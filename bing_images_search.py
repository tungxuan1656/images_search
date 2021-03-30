import requests
import shutil
from bs4 import BeautifulSoup
import os
import sys
from fake_useragent import UserAgent
from uuid import uuid4
import argparse
from tqdm import tqdm


def save_image(url, save_dir):
    # Get the file name and type
    file_name = os.path.basename(url).replace('?', '_')
    type = file_name.split(".")[-1]
    if type.lower() not in ["jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
        file_name += '.jpg'
        return

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


def bing(query, start_index=0, max_results=35):
    # set stack limit
    sys.setrecursionlimit(1000000)

    ua = UserAgent(verify_ssl=False)
    headers = {'User-Agent': ua.random}
    payload = (('q', str(query)), ('first', start_index), ('count', max_results))
    print(f'[%] Search {query}, start index: {start_index}, max result: {max_results}')
    source = requests.get("https://www.bing.com/images/async", params=payload, headers=headers).content
    soup = BeautifulSoup(str(source).replace('\r\n', ""), "lxml")

    image_urls = []
    a_images = soup.find_all("a", class_="iusc")
    print(f"[%] Found {len(a_images)} images. Get url of {max_results} images")
    for a in tqdm(a_images):
        m = list(filter(lambda x: x.startswith('"murl"'), a['m'].split(',')))
        for n in m:
            u = n[8:-1]
            image_urls.append(u)
        if len(image_urls) > max_results:
            break

    return image_urls


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Scrape images from the internet.")
    parser.add_argument(
        "query", help="Query that should be used to scrape images.", type=str)
    parser.add_argument(
        "--save_dir", help="Folder save images. If default, save to folder data/bing/{query}", default='./data/bing', type=str, required=False)
    parser.add_argument(
        "--start_index", help="Start index of images to be scraped", default=0, required=False, type=int)
    parser.add_argument(
        "--max_results", help="Amount of images to be scraped.", default=35, required=False, type=int)

    args = parser.parse_args()

    query = args.query
    save_dir = args.save_dir
    if save_dir == './data/bing':
        save_dir = f'./data/bing/{query}'
    start_index = int(args.start_index)
    max_results = int(args.max_results)

    image_urls = bing(query, start_index, max_results)
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
