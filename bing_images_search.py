from bing_search import download_image
import requests
import shutil
import json
from bs4 import BeautifulSoup
from pathlib import Path
import os
import sys
from fake_useragent import UserAgent
from uuid import uuid4


def save_image(url, save_dir):
    # Get the file name and type
    file_name = os.path.basename(url)
    type = file_name.split(".")[-1]
    if type.lower() not in ["jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
        print('[!] Error file url', url)
        return

    try:
        save_path = os.path.join(save_dir, file_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        ua = UserAgent(verify_ssl=False)
        headers = {"User-Agent": ua.random}
        r = requests.get(url, stream=True, headers=headers, timeout=30)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            raise Exception("Image returned a {} error.".format(r.status_code))
        print(f'[%] Downloaded: {url}')
    except Exception as e:
        print("[!] Issue Downloading: {}\n[!] Error: {}".format(url, e))


def bing(query, start_index=0, max_result=35):
    # set stack limit
    sys.setrecursionlimit(1000000)

    if not isinstance(query, str):
        print("Query isn't type of string class")
        return []

    if not isinstance(start_index, int) or not isinstance(max_result, int):
        print("Start Index or Max Result not is Int")
        return []

    ua = UserAgent(verify_ssl=False)
    headers = {'User-Agent': ua.random}
    payload = (('q', str(query)), ('first', start_index), ('count', max_result))
    source = requests.get("https://www.bing.com/images/async", params=payload, headers=headers).content
    soup = BeautifulSoup(str(source).replace('\r\n', ""), "lxml")

    print("\n===============================================\n")
    image_urls = []
    for a in soup.find_all("a", class_="iusc"):
        m = list(filter(lambda x: x.startswith('"murl"'), a['m'].split(',')))
        for n in m:
            u = n[8:-1]
            image_urls.append(u)
        if len(image_urls) > max_result:
            break

    return image_urls


if __name__ == '__main__':
    name = 'Cây trạng nguyên'
    image_urls = bing(name)
    for url in image_urls:
        save_image(url, f'./plant/{name}')
