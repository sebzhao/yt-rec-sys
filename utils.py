import networkx as nx
import matplotlib
import pandas as pd
from networkx.algorithms import approximation
from pyvis.network import Network
from os.path import exists

def load_graph(file_name):
    if exists(file_name):
        return nx.read_gpickle(file_name)
    else:
        print("Download from dropbox link in repo")
        return 

def most_popular_nodes(G, num_nodes = 1):
    """
    Arguments
        G: networkx object of full graph
        num_nodes: number of nodes to return
    Return
        A list of the most popular nodes in decreasing order (first subnetwork is the largest)
    """
    degree_dict = nx.in_degree_centrality(G)
    sorted_nodes = list(sorted(degree_dict, key=lambda x: degree_dict[x], reverse=True)) 
    return sorted_nodes[:num_nodes]
        
def add_attr_from_pandas(G, df, id, columns):
    for i in G:
        row = df[df[id] == i]
        for column in columns:
            G.nodes[i][column] = row[column].iloc[0]

def get_node_attributes(G, attribute):
    return [G.nodes[node][attribute] for node in G]
