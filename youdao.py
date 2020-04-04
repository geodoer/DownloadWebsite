# -*- coding: utf-8 -*-
# @Time    : 2019/11/4 8:06
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : youdao
# @Software: PyCharm
# @Version :
# @Desc    : 有道一小时内限制1000次请求，建议4秒请求一次。

import urllib.parse
import http.client
import random
import hashlib
import time


# http://ai.youdao.com
# 有道账号没钱了
appKey = '784ece665fa5e907'
secretKey = 'Ap2IyfAaaDUryMR4Q7l8u73ZGoC9vOSZ'

# 翻译网站
YOUDAO_FANYI = 'http://fanyi.youdao.com/'

# 中译英
def Ch2En(item):
    if item=="" or item is None:
        print("[有道翻译WARNING] 翻译内容出错：{}".format(item))
        return []

    time.sleep(4)
    httpClient = None
    myurl = '/api'

    fromLang = 'zh-CHS'  # 译文主体
    toLang = 'EN'  # 译文客体

    salt = random.randint(1, 65536)
    sign = appKey + item + str(salt) + secretKey
    m1 = hashlib.new('md5')
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()

    # 拼接完整译文对象
    myurl = myurl + '?appKey=' + appKey + '&q=' + urllib.parse.quote(
        item) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    result = []
    try:
        httpClient = http.client.HTTPConnection('openapi.youdao.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result = eval(response.read().decode("utf-8"))['translation']
        # print(type(result))
    except Exception as e:
        if '11001' in str(e):
            input("[网络错误] 请检查网络，按任意键继续")
            return Ch2En(item)

        print("[有道翻译ERROR] 错误{}\t翻译内容：{}".format(e, item))
        return []
    finally:
        if httpClient:
            httpClient.close()
    return result


# 英译中
def En2Ch(item):
    if item=="" or item is None:
        print("[有道翻译WARNING] 翻译内容出错：{}".format(item))
        return []

    time.sleep(4)
    httpClient = None
    myurl = '/api'

    fromLang = 'EN'     # 译文主体
    toLang = 'zh-CHS'   # 译文客体

    salt = random.randint(1, 65536)
    sign = appKey + item + str(salt) + secretKey
    m1 = hashlib.new('md5')
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl + '?appKey=' + appKey + '&q=' + urllib.parse.quote(
        item) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    result = []
    try:
        httpClient = http.client.HTTPConnection('openapi.youdao.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result = eval(response.read().decode("utf-8"))['translation']
    except Exception as e:
        if '11001' in str(e):
            input("[网络错误] 请检查网络，按任意键继续")
            return En2Ch(item)

        print("[有道翻译ERROR] 错误{}\t翻译内容：{}".format(e, item))
        return []
    finally:
        if httpClient:
            httpClient.close()
    return result

# 翻译 selenium模拟网页
# 问题：太快没有返回结果
from selenium import webdriver
def translate_selenium(item):
    if item is None or item=="": return []

    # 函数内静态变量
    if not hasattr(translate_selenium, 'driver'):
        # 创建chrome
        translate_selenium.driver = webdriver.Chrome(executable_path='../tools/chromedriver.exe')

    if translate_selenium.driver.current_url!=YOUDAO_FANYI: translate_selenium.driver.get(YOUDAO_FANYI)
    try:
        input = translate_selenium.driver.find_element_by_id("inputOriginal")
        submit = translate_selenium.driver.find_element_by_id("transMachine")
        output = translate_selenium.driver.find_element_by_id("transTarget")

        input.clear() #清空
        input.send_keys(item)
        submit.click()
        time.sleep(1)
        result = output.text

        # print(result)
    except Exception as e:
        print(e)
        return []
    finally:
        return [result]


if __name__ == '__main__':
    # c2e = Ch2En('假日')
    # print("Ch2En:", c2e)
    # e2c = En2Ch(c2e[0])
    # print("En2Ch:", e2c)

    result = translate_selenium("hello")
    print(result)


