#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 11/10/2022 3:07 PM
# @Author  : zhangbc0315@outlook.com
# @File    : fast_baidu_translate.py
# @Software: PyCharm

import json
import hashlib
import random
from pip._vendor.distlib.compat import raw_input

import requests


class FastBaiduTranslate:

    def __init__(self, app_id: str, password: str,
                 baidu_url: str = 'https://fanyi-api.baidu.com/api/trans/vip/translate'):
        self._appid = app_id
        self._password = password
        self._baidu_url = baidu_url

    def translate(self, text: str, from_lang: str = 'en', to_lang: str = 'zh'):
        # q = raw_input(text)
        q = text
        salt = random.randint(32768, 65536)
        sign_str = self._appid + q + str(salt) + self._password
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        url = self._baidu_url + f'?q={q}&from={from_lang}&to={to_lang}&appid={self._appid}&salt={salt}&sign={sign}'
        response = requests.get(url)
        res = json.loads(response.text)
        if 'trans_result' in res.keys():
            return res['trans_result'][0]['dst']
        else:
            return None


if __name__ == "__main__":
    fbt = FastBaiduTranslate('20221109001444093', 'ZKkZnZQ8nWFRH5LP2b8r')
    print(fbt.translate('I have a apple'))
