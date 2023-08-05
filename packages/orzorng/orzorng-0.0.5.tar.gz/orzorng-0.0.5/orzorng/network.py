# -*- coding: utf-8 -*-

import time
import requests

def request_api(local_sql, action, data, timeout=120):
    try:
        res = requests.post(local_sql, dict({'action': action}, **data), timeout=timeout)
        # print('ok request_api', action, res.text)
        print('ok request_api', action)
        return res
    except Exception as get_err:
        print('err request_api', local_sql, action, get_err)
        time.sleep(1)
        return request_api(local_sql, action, data, timeout)
