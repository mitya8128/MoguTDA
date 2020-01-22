
import networkx as nx
from nx import*
import networkx.algorithms.approximation as apxa
from scipy.spatial import distance
from itertools import product

from .abssimcomplex import SimplicialComplex


class VietorisRipsComplex(SimplicialComplex):
    def __init__(self,
                 points,
                 epsilon,
                 labels=None,
                 distfcn=distance.euclidean):
        self.pts = points
        self.labels = (range(len(self.pts))
                       if labels is None or len(labels) != len(self.pts)
                       else labels)
        self.epsilon = epsilon
        self.distfcn = distfcn
        self.network = self.construct_network(self.pts,
                                              self.labels,
                                              self.epsilon,
                                              self.distfcn)
        self.import_simplices(map(tuple, nx.find_cliques(self.network)))

    def construct_network(self, points, labels, epsilon, distfcn):
        g = nx.Graph()
        g.add_nodes_from(labels)
        zips = zip(points, labels)
        for pair in product(zips, zips):
            if pair[0][1] != pair[1][1]:
                dist = distfcn(pair[0][0], pair[1][0])
                if dist < epsilon:
                    g.add_edge(pair[0][1], pair[1][1])
        return g


    def clustering(self):
        graph = self.construct_network()
        clustering_coef = nx.average_clustering(graph)
        return clustering_coef


    def edge_cover(self):
        graph = self.construct_network()
        cover_edge = nx.min_edge_cover(graph)
        return cover_edge


    def ramsey(self):
        graph = self.construct_network()
        numbers = nx.algorithms.approximation.ramsey_R2(graph)
        return numbers


    def independent(self):
        graph = self.construct_network()
        independent_set = nx.maximal_independent_set(graph)
        return independent_set


    def dominating(self):
        graph = self.construct_network()
        dominating_set = nx.algorithms.approximation.min_edge_dominating_set(graph)
        return dominating_set

    def vertex_cover(self):
        graph = self.construct_network()
        cover_vertex = nx.algorithms.approximation.min_weighted_vertex_cover(graph)    # weight = None
        return cover_vertex
