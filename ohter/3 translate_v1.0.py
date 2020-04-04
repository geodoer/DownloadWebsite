# -*- coding: utf-8 -*-
# @Time    : 2019/11/4 8:10
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : TranslateWebsite
# @Software: PyCharm
# @Version :
# @Desc    :

import youdao
import os
import shutil
from tqdm import tqdm
from bs4 import BeautifulSoup


WEBSITE_PATH = 'geomesa_en' #原地址
SAVE_PATH = 'geomesa_ch'    #翻译结果

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        # print("[OK] Create Dir:{}".format(path) )
        return True
    else: #已经存在
        return False

def copyfile(srcfile,dstfile):
    if os.path.exists(dstfile):
        print("[WARNING] {} is exist".format(dstfile))
        return
    if not os.path.isfile(srcfile):
        print("[ERROR] %s not exist!"%(srcfile))
        return
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(srcfile,dstfile)
        print("[OK] copy %s -> %s"%(srcfile, dstfile) )
        return

def translate_html(in_path, out_path):
    if os.path.exists(out_path): return

    # [测试] translate_html("geomesa_en\user\lambda\advanced.html", "geomesa_ch\user\lambda\advanced.html")
    # print("[translate] {} {}".format(in_path, out_path))
    in_fp = open(in_path, 'r', encoding="utf-8")
    soup = BeautifulSoup(in_fp.read(), 'html.parser')
    for tag in tqdm(soup.findAll('p'), "{}".format(in_path)):
        text = tag.get_text()
        result = youdao.En2Ch(text)
        if len(result)>0:
            tag.string = result[0]

    # 保存
    mkdir(os.path.dirname(out_path) )
    html = soup.prettify("utf-8")
    with open(out_path, "wb") as out_fp:
        out_fp.write(html)

if __name__ == '__main__':
    mkdir(WEBSITE_PATH)

    # 翻译单个网页
    # translate_html(r"geomesa_en\user\lambda\advanced.html", r"geomesa_ch\user\lambda\advanced.html")

    # 扫描文件夹下的HTML文件
    htmls = []
    for root, dirs, files in os.walk(WEBSITE_PATH):
        for file in files:
            in_fp = os.path.join(root, file)
            out_fp = os.path.join(root.replace(WEBSITE_PATH, SAVE_PATH), file)
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
        translate_html(in_fp, out_fp)