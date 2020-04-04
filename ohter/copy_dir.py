# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 11:55
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : copy_dir
# @Software: PyCharm
# @Version :
# @Desc    :

import os
import shutil

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


website_path = r"D:\mycode\GetAllWebPage\result_save\geomesa_ch_back_20191104"
save_path = r"D:\mycode\GetAllWebPage\result_save\geomesa_ch"

for root, dirs, files in os.walk(website_path):
    for file in files:
        in_fp = os.path.join(root, file)
        out_fp = os.path.join(root.replace(website_path, save_path), file)
        copyfile(in_fp, out_fp)