# -*- coding: utf-8 -*-
# @Time    : 2019/11/4 18:51
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : 3 translate_v2.0
# @Software: PyCharm
# @Version :
# @Desc    : 就地翻译 | 复制翻译 两种方案

import youdao
import os
import shutil
from tqdm import tqdm
import json
from bs4 import BeautifulSoup


WEBSITE_PATH = 'geomesa_ch' # 原地址
SAVE_PATH = 'geomesa_ch'    # 翻译结果
# 注：WEBSITE_PATH，SAVE_PATH设置成一样即可就地翻译（翻译内容保存到原文件加下）
READ_HISTORY = False        # 就地翻译是否读历史记录（True：接着上次的翻译）


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        # print("[OK] Create Dir:{}".format(path) )
        return True
    else:  # 已经存在
        return False


def copyfile(srcfile, dstfile):
    if os.path.exists(dstfile):
        print("[WARNING] {} is exist".format(dstfile))
        return
    if not os.path.isfile(srcfile):
        print("[ERROR] %s not exist!" % (srcfile))
        return
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(srcfile, dstfile)
        print("[OK] copy %s -> %s" % (srcfile, dstfile))
        return

def load_json(fp):
    with open(fp, 'r') as f:
        return json.load(f)
def save_json(fp, obj):
    if os.path.exists(fp):
        os.remove(fp)
    with open(fp, 'w+') as f:
        json.dump(obj, f, indent=4)
        f.close()

def translate_html(in_path, out_path):
    # [测试] translate_html("geomesa_en\user\lambda\advanced.html", "geomesa_ch\user\lambda\advanced.html")
    # print("[translate] {} {}".format(in_path, out_path))
    in_fp = open(in_path, 'r', encoding="utf-8")
    soup = BeautifulSoup(in_fp.read(), 'html.parser')
    for tag in tqdm(soup.findAll('p'), "{}".format(in_path)):
        text = tag.get_text()
        result = youdao.En2Ch(text)
        if len(result) > 0:
            tag.string = result[0]

    # 保存
    mkdir(os.path.dirname(out_path))
    html = soup.prettify("utf-8")
    with open(out_path, "wb") as out_fp:
        out_fp.write(html)

# 翻译到save_path
def translate_website_copy(website_path, save_path):
    # 扫描文件夹下的HTML文件
    htmls = []
    for root, dirs, files in os.walk(website_path):
        for file in files:
            in_fp = os.path.join(root, file)
            out_fp = os.path.join(root.replace(website_path, save_path), file)
            if file.endswith('html'):  # 网站
                htmls.append([in_fp, out_fp])
            else:  # 其他文件：复制
                copyfile(in_fp, out_fp)
    print(htmls)
    # 开始翻译
    for html in tqdm(htmls, "HTML进程"):
        if (len(html) != 2): continue
        in_fp = html[0]
        out_fp = html[1]
        if os.path.exists(out_fp): continue
        translate_html(in_fp, out_fp)

# 就地翻译
def translate_website(website_path, read_history=True):
    ok = []
    history_path = os.path.join(website_path, "hisotry.json")
    if READ_HISTORY and os.path.exists(history_path): ok = load_json(history_path)

    try:
        htmls = []
        for root, dirs, files in os.walk(website_path):
            for file in files:
                if file.endswith('html'):  # 网站
                    in_fp = os.path.join(root, file)
                    htmls.append(in_fp)
        print(htmls)

        # 开始翻译
        for html in tqdm(htmls, "HTML进程"):
            if html in ok: continue
            translate_html(html, html)
            ok.append(html)
    except Exception as e:
        save_json(history_path, ok)
        print(e)
    finally:
        save_json(history_path, ok)


if __name__ == '__main__':
    # 翻译单个网页
    # translate_html(r"geomesa_en\user\lambda\advanced.html", r"geomesa_ch\user\lambda\advanced.html")

    # 翻译网站（多个HTML）
    if WEBSITE_PATH==SAVE_PATH:
        # 就地翻译
        translate_website(WEBSITE_PATH, READ_HISTORY)
    else:
        # 翻译到SAVE_PATH
        translate_website_copy(WEBSITE_PATH, SAVE_PATH)