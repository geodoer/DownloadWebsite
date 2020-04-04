# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 9:17
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : 3 translate_v4.0
# @Software: PyCharm
# @Version :
# @Desc    : 1. 抽取指定文件夹内指定格式的文件的指定内容，并保存成excel
#            2. 用youdao.py翻译此excel
#            3. 参考excel中翻译内容，替换文件中的内容

import youdao
import os
from tqdm import tqdm
import json
from bs4 import BeautifulSoup
import pandas as pd

WEBSITE_PATH = r'D:\mycode\GetAllWebPage\geomesa_ch' #网站地址
# 高级设置
OK_HISOTRY = True         #读翻译的历史记录
FORMATS = ['html', 'htm']   #格式

# global
ok_path = os.path.join(WEBSITE_PATH, "history.json")
word_path = os.path.join(WEBSITE_PATH, "words.xls")
cols_name = [u'原文', u'译文'] #excel中的列名

# tools
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


def get_ok():
    # 读已经翻译的历史文件
    if OK_HISOTRY and os.path.exists(ok_path):
        ok = load_json(ok_path)
    else:
        ok = []
    return ok

def get_words():
    if os.path.exists(word_path):
        word_df = pd.read_excel(word_path)
    else: #创建两个空列
        word_df = pd.DataFrame(columns=cols_name )
    return word_df


# 要翻译的标签
def process_soup(soup):
    return soup.findAll('p')

# 得到website_path下要翻译的内容，加到df中
def get_translate_tonext():
    global  WEBSITE_PATH
    global  FORMATS

    word_df = get_words()
    files = []

    # 找到所有指定文件
    for tmp_root, tmp_dirs, tmp_files in os.walk(WEBSITE_PATH):
        for tmp_file in tmp_files:
            # 格式筛选
            format = tmp_file.split('.')[-1]
            if format not in FORMATS:
                continue

            files.append(os.path.join(tmp_root, tmp_file))

    # 遍历文件
    for file in tqdm(files, "获得要翻译的内容"):
        fpath = os.path.join(WEBSITE_PATH, file)
        fp = open(fpath, 'r', encoding="utf-8")
        soup = BeautifulSoup(fp.read(), 'html.parser')
        tags = process_soup(soup)
        for tag in tags:
            text = tag.get_text()

            # 过滤不要翻译的内容
            if text is None or text is "" or text is "\n": continue
            result_df = word_df[ word_df[cols_name[0]]==text] #查找是否已经存在
            if result_df.empty == False: #已经存在
                continue

            new_line = {cols_name[0]:text, cols_name[1]:"" }
            word_df = word_df.append(new_line, ignore_index=True)

    # 保存df
    word_df.to_excel(word_path)
    pass



# 翻译excel内的东西
def translate():
    word_df = get_words()

    # 转换成list翻译
    # words = word_df.values.tolist()
    # for row in tqdm(words, "开始翻译文本"):
    #     item = row[0]
    #     result = youdao.En2Ch(item)
    #     if len(result)>0:
    #         row[1] = result[0] #添加翻译结果
    #     else:
    #         row[1] = None #无内容
    # new_word_df = pd.DataFrame(data=words, columns=cols_name)
    # new_word_df.to_excel(word_path)

    total = word_df.shape[0]
    pbar = tqdm(total=total) #总行数
    for i,row in word_df.iterrows():
        item = row[ cols_name[0] ]
        # 不翻译
        if not pd.isnull(row[cols_name[1]]) or row[cols_name[1]]=="":
            continue

        result = youdao.translate_selenium(item)
        if len(result) > 0:
            row[cols_name[1]] = str(result[0]) #添加翻译结果
            pbar.desc = result[0]
        else:
            row[cols_name[1]] = ""
            pbar.desc = "翻译失败"

        # 翻译了50条保存一次
        if i % 50 == 0: word_df.to_excel(word_path)
        pbar.update(i)

    # 完成
    pbar.update(total)
    pbar.close()
    word_df.to_excel(word_path)

# 将excel里的内容替换
def replace():
    word_df = get_words()
    files = []

    # 找到所有指定文件
    for tmp_root, tmp_dirs, tmp_files in os.walk(WEBSITE_PATH):
        for tmp_file in tmp_files:
            # 格式筛选
            format = tmp_file.split('.')[-1]
            if format not in FORMATS:
                continue

            files.append(os.path.join(tmp_root, tmp_file))

    # 遍历文件
    for file in tqdm(files, "替换文件内容"):
        fpath = os.path.join(WEBSITE_PATH, file)
        fp = open(fpath, 'r', encoding="utf-8")
        soup = BeautifulSoup(fp.read(), 'html.parser')
        tags = process_soup(soup)
        for tag in tags:
            text = tag.get_text()

            # 获得翻译
            result_df = word_df[word_df[cols_name[0]] == text]  # 查找是否已经存在
            if result_df.empty: #不存在
                continue
            result = result_df.values.tolist()
            result_text = result[0][1]

            tag.string = str(result_text)

        # 保存
        html = soup.prettify("utf-8")
        with open(fpath, "wb") as out_fp:
            out_fp.write(html)
    pass





if __name__ == '__main__':
    # UI
    # 得到要翻译的内容
    # if input('输入1：得到指定文本（将要翻译的内容）\n输入其他跳过此步\n')=='1':
    #     get_translate_tonext()
    # # 翻译
    # if input('输入1：开始翻译单词表\n输入其他跳过此步\n')=='1':
    #     translate()
    # # 替换到HTML
    # if input('输入1：开始替换本文内容\n输入其他跳过此步\n')=='1':
    #     replace()

    # debug
    # get_translate_tonext()
    translate()
    # replace()


    pass