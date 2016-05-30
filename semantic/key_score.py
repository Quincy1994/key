__author__ = 'kalin'
# coding=utf-8
from betweenness_centrality import *
from collections import Counter
from candidate_words import *
import os
import time
import jieba.analyse

class Keyword():

    def __init__(self):
        self.poss = {}   #词性表
        self.word_length={}
        self.word_score = {}

    def feature(self, string_data):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, 'tag.txt')
        files = open(file_path, "r")
        file = files.readlines()
        for line in file:
            s = line.strip().split(' ')
            self.poss[s[0]] = s[1]
        po = self.poss
        candidate_words_dict, nword = CandidateWords().get_candidate_list(string_data)
        nwword_words = nword.values()   #order words
        pos = {}
        for word in nwword_words:
            self.word_length[word] = len(word)/3
            if candidate_words_dict[word] in po.keys():
                pos[word] = float(po[candidate_words_dict[word]])
            else:
                pos[word] = 0.1
        words_tf_dict = dict(Counter(nwword_words))
        files.close()
        return (pos, words_tf_dict, self.word_length, nwword_words)

    def score(self, string_data):
        tw = 0.4
        vdw = 0.6
        lenw = 0.1
        posw = 0.8
        tfw = 0.3
        pos, words_tf_dict, word_length, candidate_word = self.feature(string_data)
        vd = BetweenCentrality().codes_betweeness_centarlity(string_data)
        for word in candidate_word:
            s = (vd[word] * vdw ) + (tw * (word_length[word] * lenw + pos[word] * posw + words_tf_dict[word]*tfw))
            self.word_score[word] = s
        rank = sorted(self.word_score.iteritems(), key=lambda d: d[1], reverse=True)
        return rank

    def keyword(self, string_data):
            key_score = self.score(string_data)
            keywords = []
            for key in key_score[0:7]:
                keywords.append(key[0])
            return keywords, key_score

import json
import requests


def bosonNLP(text):
    KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'
    params = {'top_k': 10}
    data = json.dumps(text)
    headers = {'X-Token': 'rHcI_KOq.3981.L8neAWDOzSsE'}
    resp = requests.post(KEYWORDS_URL, headers=headers, params=params, data=data.encode('utf-8'))
    for weight, word in resp.json():
        print word,

if __name__ == "__main__":
    string = '郑州大学的一位男生暗恋一位女生，这是他写给她的情书，真好，我都快融化了，真想知道他们在一起了吗？！'
    keyword_list = Keyword().keyword(string)
    for key in keyword_list:
        print key,
    print '\n'
    keyword_list = jieba.analyse.extract_tags(string)
    for key in keyword_list:
        print key,
    print '\n'
    bosonNLP(string)


