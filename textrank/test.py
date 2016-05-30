# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests


def bosonNLP(filename):
    text = open(filename).read()
    KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'
    params = {'top_k': 10}
    data = json.dumps(text)
    headers = {'X-Token': 'rHcI_KOq.3981.L8neAWDOzSsE'}
    resp = requests.post(KEYWORDS_URL, headers=headers, params=params, data=data.encode('utf-8'))
    for weight, word in resp.json():
        print(weight, word)

if __name__ == '__main__':
    filename = '/home/quincy1994/桌面/test.txt'
    bosonNLP(filename)