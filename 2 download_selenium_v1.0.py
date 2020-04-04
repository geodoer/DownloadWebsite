# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 20:56
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : DownloadWebsite
# @Software: PyCharm
# @Version :
# @Desc    :

import time
from selenium import webdriver
import os
import json
from tqdm import tqdm

DOMAIN = 'https://www.geomesa.org/documentation/' #爬取的域名，最后要有'/'
SAVE_DIR = 'geomesa_en' #保存路径

def load_json(fp):
    with open(fp, 'r') as f:
        return json.load(f)
def save_json(fp, obj):
    if os.path.exists(fp):
        os.remove(fp)
    with open(fp, 'w+') as f:
        json.dump(obj, f, indent=4)
        f.close()
    return fp
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        # print("[OK] Create Dir:{}".format(path) )
        return True
def get_save_path(url):
    fn = url.split('/')[-1]
    prefix = url.replace(DOMAIN, '').replace(fn, '')
    dir = os.path.join(SAVE_DIR, prefix)
    fp = os.path.join(dir, fn)
    mkdir(dir) #创建保存目录
    return fp,dir,fn
def save_url(url):
    fp, dir, fn = get_save_path(url) #获得本地保存路径
    if os.path.exists(fp):
        # print("[is exists] {} {}".format(url, fp))
        return fp

    driver.get(url)
    time.sleep(5)
    context = driver.page_source
    with open(fp, 'w', encoding="utf-8") as file:
        file.write(context)
        file.close()
    # print("[save] {} {}".format(url, fp))
    return fp

from urllib.request import urlretrieve
def save_file(url):
    fp, dir, fn = get_save_path(url)
    # 检查路径是否存在
    if os.path.exists(fp):
        # 已经存在
        # print("[is exists] {} {}".format(url, fp))
        return fp
    # 下载
    urlretrieve(url, fp)
    # print("[save] {} {}".format(url, fp))

if __name__ == '__main__':
    visit_path = os.path.join(SAVE_DIR, "visit.json")
    img_path = os.path.join(SAVE_DIR, "img.json")
    assets_path = os.path.join(SAVE_DIR, "assets.json")

    driver = webdriver.Chrome(executable_path='../tools/chromedriver.exe')
    # 网速太慢需要等待
    driver.set_page_load_timeout(10 * 60)
    driver.set_script_timeout(10 * 60)

    print("\ndownload img")
    if os.path.exists(img_path):
        img_urls = load_json(img_path)
        for img in tqdm(img_urls):
            save_file(img)

    print("\ndownload assets")
    if os.path.exists(assets_path):
        other_assets = load_json(assets_path)
        for url in tqdm(other_assets):
            if DOMAIN in url:
                save_file(url)

    print("\ndownload html")
    if os.path.exists(visit_path):
        visit_list = load_json(visit_path)
        for html in tqdm(visit_list):
            save_url(html)

    pass