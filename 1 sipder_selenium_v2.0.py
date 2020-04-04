# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 7:50
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : DownloadHTML_selenium
# @Software: PyCharm
# @Version :
# @Desc    :
#   1. [selenium] https://selenium-python.readthedocs.io/
#   2. [start] doc->python开始selenium
# @Problem：v1.0边爬边保存，中间出现异常就麻烦
# @Improve：v2.0 [解耦合] 先爬生成urls的表单，再依次下载
# @Problem: v2.0 只能扫描HTML内部标签加载的静态资源，而在js里加载的css、js文件无法扫描到
# @Imporve：[未实施]用从selenium中获得依赖的静态资源列表

import time
from selenium import webdriver
import os
import json

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
def get_ele_url(ele):
    # https://www.geomesa.org/documentation/
    url =  ele.get_attribute('href')
    if url is None:
        url = ele.get_attribute('src')
    return url


def process(url):
    if type(url) is not str:
        return []

    driver.get(url)
    time.sleep(2)

    # 图片
    for img in driver.find_elements_by_tag_name('img'):
        img_url = get_ele_url(img)

        # 保存img的url
        if 'http' not in img_url:
            img_url = os.path.join(url, img_url)
        if img_url not in img_urls: img_urls.append(img_url)


    # url
    urls = []
    for script in driver.find_elements_by_tag_name('script'): # <script>
        tmp_url = get_ele_url(script)
        urls.append(tmp_url)

    for a in driver.find_elements_by_tag_name('a'): #a
        tmp_url = get_ele_url(a)
        urls.append(tmp_url)


    for link in driver.find_elements_by_tag_name('link'): # <link>
        tmp_url = get_ele_url(link)
        urls.append(tmp_url)

    ret_urls = []
    for tmp_url in urls:
        if type(tmp_url) is not str:
            continue
        if tmp_url.endswith('html') and DOMAIN in tmp_url:
            if tmp_url not in ret_urls: ret_urls.append(tmp_url)
        elif '#' in tmp_url: continue
        else:
            if tmp_url not in other_assets: other_assets.append(tmp_url)


    return ret_urls

img_urls = []       #img的url
other_assets = []   #其他资源的url
visit = []  #已访问队列
next = []   #下一个Url
def spider(start_url):
    ''' 爬虫
    :param start_url: 开始的url
    :return:
    '''
    global img_urls, other_assets, visit, next

    # 获得历史记录
    visit_path = os.path.join(SAVE_DIR, "visit.json")
    next_path = os.path.join(SAVE_DIR, "next.json")
    img_path = os.path.join(SAVE_DIR, "img.json")
    assets_path = os.path.join(SAVE_DIR, "assets.json")
    if os.path.exists(visit_path): visit = load_json(visit_path)
    if os.path.exists(next_path): next = load_json(next_path)
    if os.path.exists(img_path): img_urls = load_json(img_path)
    if os.path.exists(assets_path): other_assets = load_json(assets_path)

    next.append(start_url)
    try:
        while len(next):
            current_url = next[0] #取第一个的URL
            if current_url in visit: #访问过了
                next.remove(current_url)
                continue
            else: #还没访问
                urls = process(current_url) #处理该网页
                for url in urls:
                    if url not in visit and url not in next:
                        next.append(url)
                # 此页面处理完成
                next.remove(current_url)
                visit.append(current_url)

                # print
                print('--- {}'.format(current_url))
                print('[next]\t{}\t{}'.format(len(next), next) )
                print('[imgs]\t{}\t{}'.format(len(img_urls), img_urls) )
                print('[assets]\t{}\t{}'.format(len(other_assets), other_assets))
                print('[visit]\t{}\t{}'.format(len(visit), visit) )

    except Exception as e:
        # 异常，保存历史记录
        save_json(visit_path, visit)
        save_json(next_path, next)
        save_json(assets_path, other_assets)
        save_json(img_path, img_urls)
        print(e )
        pass
    finally:
        save_json(visit_path, visit)
        save_json(next_path, next)
        save_json(assets_path, other_assets)
        save_json(img_path, img_urls)
        pass

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=r'D:\mycode\PythonGISWeb\tools\chromedriver.exe')
    # 网速太慢需要等待
    driver.set_page_load_timeout(10*60)
    driver.set_script_timeout(10*60)
    # 开始爬取
    start_url = "https://www.geomesa.org/documentation/index.html"
    spider(start_url)