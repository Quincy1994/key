__author__ = 'kalin'
# coding=utf-8
import jieba.posseg as pseg      #words tagging
import os


class CandidateWords:

        def __init__(self):
            self. stopws = []
            self.candidate_word = []    #order
            self.flag = []
            self.candidate_dict = {}
            self.nword = {}

        def stopwd(self):
            base_dir = os.path.dirname(__file__) #获取当前文件夹的绝对路径
            file_path = os.path.join(base_dir, 'stopwords.txt')  #获取当前文件夹内的文件
            files = open(file_path, "r") #读取文件
            stopword = files.readlines()
            for line in stopword:
                sw = line.strip('\n')
                sw = sw.decode('utf-8')# type is str
                self.stopws.append(sw)
            files.close()
            return self.stopws

        def get_candidate_list(self, string_data):
            stop = self.stopwd()
            words_tag = pseg.cut(string_data)
            for w in words_tag:
                if w.flag != u'x' and (w.word not in stop):
                    self.candidate_word.append(w.word.encode("utf-8"))
                    self.flag.append(w.flag.encode("utf-8"))
            for i in range(len(self.flag)):
                self.candidate_dict[self.candidate_word[i]] = self.flag[i]   #disorder dict (word:flag)
            for i in range(len(self.candidate_word)):
                self.nword[i] = self.candidate_word[i]
            return self.candidate_dict, self.nword

