# -*- coding: utf-8 -*-
# @Time    : 2019/11/2 19:45
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : 下载网页
# @Software: PyCharm
# @Version :
# @Desc    :

import urllib.request


def get_html(url):
    html = urllib.request.urlopen(url).read()
    return html

def save_html(file_name, file_content):
    # 注意windows文件命名的禁用符，比如 /
    with open(file_name.replace('/', '_') + ".html", "wb") as f:
        # 写文件用bytes而不是str，所以要转码
        f.write(file_content)




aurl = "https://www.geomesa.org/documentation/user/architecture.html#geomesa-and-geoserver"
html = get_html(aurl)
save_html("sduview", html)

print("下载成功")