#coding=utf-8
import jieba
import copy
from igraph import *
import operator



class ReverseIndex:

    def __init__(self, string):
        self.dict_wordindex = {}
        self.documents = []
        self.load_data(string)


    def load_data(self, string):
        self.documents = string.split('，|？|！|。|；')

    def index(self):
        for doc in self.documents:
            words = jieba.cut(doc)
            for word in words:
                newword = word.encode('utf-8')
                if newword.__len__() < 4:
                    continue
                if newword not in self.dict_wordindex:
                    self.dict_wordindex[newword] = []
                self.dict_wordindex[newword].append(self.documents.index(doc))
        return self.dict_wordindex


class TextRank:

    def __init__(self, dict_wordindex):
        self.dict_wordindex = dict_wordindex
        self.set_wordindex = self.getSetWordIndex(dict_wordindex)
        self.graph, self.weights, self.listword = self.getRelatedGraph(self.set_wordindex)

    def getSetWordIndex(self, dict_wordindex):
        set_wordindex = copy.deepcopy(dict_wordindex)
        for word in set_wordindex:
            set_wordindex[word] = set(set_wordindex[word])
        return set_wordindex

    def getRelatedGraph(self, set_wordindex):
        list_word = set_wordindex.keys()
        nodes = self.set_wordindex.__len__()
        graph = Graph(nodes)
        graph.vs["name"] = list_word
        edges = []
        weights = []
        for i in range(0, nodes, 1):
            for j in range(0, nodes, 1):
                if i == j:
                    continue
                weight = (self.set_wordindex[list_word[i]] & self.set_wordindex[list_word[j]]).__len__()
                if weight > 0:
                    tf = self.dict_wordindex[list_word[i]].__len__()
                    df = self.set_wordindex[list_word[i]].__len__()
                    weight = tf * weight * df
                    edges += [(i, j)]
                    weights.append(weight)
        graph.add_edges(edges)
        return graph, weights, list_word

    def ranking(self, attribute="pagerank"):
        if attribute == "authority_score":
            list_ranking = self.graph.authority_score(weights=self.weights)
        elif attribute == "hub_score":
            list_ranking = self.graph.hub_score(weights=self.weights)
        elif attribute == "pagerank":
            list_ranking = self.graph.pagerank(weights=self.weights)
        elif attribute == "degree":
            list_ranking = self.graph.degree()
        elif attribute == "betweeness":
            list_ranking = self.graph.betweenness()
        elif attribute == "closeness":
            list_ranking = self.graph.closeness()
        elif attribute == "evcent":
            list_ranking = self.graph.evcent()
        else:
            list_ranking = None
        return list_ranking

    def findTopK(self, attribute, topk):
        list_ranking = self.ranking(attribute)
        dict_ranking = {}
        for i in range(0, list_ranking.__len__(), 1):
            dict_ranking[i] = list_ranking[i]
        sorted_ranking = sorted(dict_ranking.iteritems(), key=operator.itemgetter(1),reverse=True)
        list_top = []
        for i in sorted_ranking:
            list_top.append(self.listword[i[0]])
        return list_top[0:topk]





if __name__ == '__main__':
    string='郑州大学的一位男生暗恋一位女生，这是他写给她的情书，真好，我都快融化了，真想知道他们在一起了吗？！'
    reindex = ReverseIndex(string)
    dict_wordindex = reindex.index()
    textrank = TextRank(dict_wordindex)
    list_top = textrank.findTopK('pagerank', 5)
    for key in list_top:
        print key,