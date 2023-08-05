# -*- coding: utf-8 -*-

import os
import re

from .file import get_file_line


def is_ip(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False


# 判断数据是否在数据里面
def is_res(type, str):
    for item in get_file_line(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', type + '.data')):
        if item in str:
            return item

    return False


# 字符串只保留中文
def only_zh(str):
    return re.sub('[^\u4e00-\u9fa5]+', '', str)

# 去除特殊字符
def delete_boring_characters(sentence):
    return re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", sentence)
    # return re.sub('[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", sentence)
