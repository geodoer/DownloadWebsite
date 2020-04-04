# -*- coding: utf-8 -*-
# @Time    : 2019/11/4 18:51
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : 3 translate_v2.0
# @Software: PyCharm
# @Version :
# @Desc    : 抛弃复制翻译，只保留就地翻译
# @Proplem ：有道限制每小时1000次
# @Improve ：1. 多个KEY
#            2. 先获得网页内所有要翻译结果，并去重；统一翻译保存；统一替换

import youdao
import os
from tqdm import tqdm
import json
from bs4 import BeautifulSoup
import datetime


WEBSITE_PATH = 'geomesa_ch' #网站地址
# 高级设置
READ_HISTORY = True         #是否读历史记录
FORMAT = ['html', 'htm']    #格式

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        # print("[OK] Create Dir:{}".format(path) )
        return True
    else:  # 已经存在
        return False
def load_json(fp):
    with open(fp, 'r') as f:
        return json.load(f)
def save_json(fp, obj):
    if os.path.exists(fp):
        os.remove(fp)
    with open(fp, 'w+') as f:
        json.dump(obj, f, indent=4)
        f.close()


def translate_html(path):
    # [测试] translate_html("geomesa_en\user\lambda\advanced.html", "geomesa_ch\user\lambda\advanced.html")
    # print("[translate] {} {}".format(in_path, out_path))
    context = [] #记录该页面所有翻译结果

    in_fp = open(path, 'r', encoding="utf-8")
    soup = BeautifulSoup(in_fp.read(), 'html.parser')
    for tag in tqdm(soup.findAll('p'), "{}".format(path)):
        text = tag.get_text()
        result = youdao.En2Ch(text)
        if len(result) > 0:
            tag.string = result[0]
            context.append([path, text, result[0] ] )

    # 保存
    html = soup.prettify("utf-8")
    with open(path, "wb") as out_fp:
        out_fp.write(html)
    return context

# 就地翻译
def translate_website(website_path, read_history=True, formats=['html']):
    ok = [] #记录已经翻译的页面
    # 历史记录
    history_path = os.path.join(website_path, "hisotry.json")
    if read_history and os.path.exists(history_path): ok = load_json(history_path)
    # 记录此次翻译结果
    translate_result = []

    try:
        # 获得website_path下所有HTML
        htmls = []
        for root, dirs, files in os.walk(website_path):
            for file in files:
                for format in formats:
                    if file.endswith(format):  # 网站
                        in_fp = os.path.join(root, file)
                        htmls.append(in_fp)
        print("[{}] {}".format(len(htmls), htmls) )

        # 开始翻译
        for html in tqdm(htmls, "HTML进程"):
            if html in ok: continue
            context = translate_html(html) #得到全部翻译结果
            translate_result = translate_result + context
            ok.append(html)
    except Exception as e:
        save_json(history_path, ok)
        print(e)
    finally:
        import pandas as pd
        save_json(history_path, ok)
        # 保存所有翻译结果
        print(translate_result)

        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        translate_path = os.path.join(website_path, "翻译结果{}.xls".format(current_time))
        df = pd.DataFrame(columns=["文件路径", "原文", "翻译结果"], data=translate_result)
        df.to_excel(translate_path)


if __name__ == '__main__':
    # 翻译单个网页
    # translate_html(r"geomesa_en\user\lambda\advanced.html", r"geomesa_ch\user\lambda\advanced.html")

    translate_website(WEBSITE_PATH, READ_HISTORY, FORMAT)