__author__ = 'kalin'
# coding=utf-8
import networkx as nx
from semantic_similarity_network import *
from candidate_words import *


class BetweenCentrality:

    def __init__(self):
        self.G = nx.Graph()
        self.bcdict = {}
        self.nword = {}

    def codes_betweeness_centarlity(self, string_data):
            candidate_words_dict, nwword = CandidateWords().get_candidate_list(string_data)
            nwword_words=nwword.values()
            length = len(nwword_words)
            for i in range(length):
                self.G.add_node(i)
            E = Semantic_similarity().similarity_network_edges(string_data)
            self.G.add_edges_from(E)
            vd= nx.betweenness_centrality(self.G, k=None, normalized=True, weight=None, endpoints=False, seed=None )
            for i in range(length):
                self.bcdict[nwword_words[i]] = vd[i]
            for i in range(length):
                self.nword[i] = nwword_words[i]
            return self.bcdict  #type is dict

