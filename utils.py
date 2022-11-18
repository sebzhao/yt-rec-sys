import networkx as nx
import matplotlib
import pandas as pd
from networkx.algorithms import approximation
from pyvis.network import Network
from os.path import exists
import datetime
import seaborn as sns

def load_graph(file_name):
    """
    Loads graph given by file_name

    Arguments
        file_name: file path to the networkx graph pickle file
    Returns
        Loaded graph from `file_name` pickle file
    """
    if exists(file_name):
        return nx.read_gpickle(file_name)
    else:
        print("Download " + file_name + " from dropbox link in repo")
        return 

def most_popular_nodes(G, num_nodes = 1):
    """
    Finds num_nodes most popular nodes of G as determined by number of recommendations

    Arguments
        G: networkx object of full graph
        num_nodes: number of nodes to return
    Returns
        A list of the most popular nodes in decreasing order (first subnetwork is the largest)
    """
    degree_dict = nx.in_degree_centrality(G)
    sorted_nodes = list(sorted(degree_dict, key=lambda x: degree_dict[x], reverse=True)) 
    return sorted_nodes[:num_nodes]
        
def add_attr_from_pandas(G, df, id, columns):
    """
    Adds node attributes to G from a df

    Arguments
        G: networkx graph
        df: dataframe holding node attributes
        id: name of column in `df` that specifies the shared pks between 
            `df` and nodes in `G`
        columns: list of column names in `df` that should be added to the graph
    Returns
        None, modifies G in place
    """
    for i in G:
        row = df[df[id] == i]
        for column in columns:
            G.nodes[i][column] = row[column].iloc[0]

def get_node_attributes(G, attribute):
    """
    Gets all values of a node attribute from G if not None

    Arguments
        G: networkx graph
        attribute: name of the node attribute in `G`
    Returns
        List of the specific attribute from all nodes in `G`
    """
    return [G.nodes[node][attribute] for node in G if G.nodes[node][attribute] != None]

def add_predecessor_attribute(G, attribute, agg, name):
    """
    Adds a predecessor summary stat of attribute to G aggregated by agg
    invalid values are filled in as None.

    Arguments
        G: networkx graph
        attribute: name of the node attribute in `G`
        agg: function to aggregate all of the predecessor values of `attribute`
        name: name of new attribute to be made
    Returns
        None, modifies G in place
    """
    for node in G:
        pred_res = []
        preds = G.predecessors(node)
        for pred in preds:
            pred_res.append(G.nodes[pred][attribute])
        if pred_res:
            G.nodes[node][name] = agg(pred_res)
        else:
            G.nodes[node][name] = None

def add_successor_attribute(G, attribute, agg, name):
    """
    Adds a successor summary stat of attribute to G aggregated by agg
    invalid values are filled in as None.

    Arguments
        G: networkx graph
        attribute: name of the node attribute in `G`
        agg: function to aggregate all of the successor values of `attribute`
        name: name of new attribute to be made
    Returns
        None, modifies G in place
    """
    for node in G:
        succ_res = []
        succs = G.successors(node)
        for succ in succs:
            succ_res.append(G.nodes[succ][attribute])
        if succ_res:
            G.nodes[node][name] = agg(succ_res)
        else:
            G.nodes[node][name] = None

def convert_to_datetime(G, attribute):
    """
    Converts string attribute in graph to datetime. 

    Arguments:
        G: networkx graph
        attribute: name of the node attribute in `G`
    Returns
        None, modifies G in place
    """
    for node in G:
        G.nodes[node][attribute] = datetime.strptime(G.nodes[node][attribute], '%Y-%m-%d')

def add_predecessor_time_diff(G, attribute, agg, name):
    """
    Adds a predecessor summary stat of time difference from node to predecessor to G aggregated by agg
    invalid values are filled in as None.

    Arguments
        G: networkx graph
        attribute: name of the node attribute in `G`
        agg: function to aggregate all of the predecessor values of `attribute`
        name: name of new attribute to be made
    Returns
        None, modifies G in place
    """
    for node in G:
        pred_res = []
        preds = G.predecessors(node)
        for pred in preds:
            pred_res.append((G.nodes[node][attribute] - G.nodes[pred][attribute]).days)
        if pred_res:
            G.nodes[node][name] = agg(pred_res)
        else:
            G.nodes[node][name] = None

def add_successor_time_diff(G, attribute, agg, name):
    """
    Adds a successor summary stat of time difference from node to successor to G aggregated by agg
    invalid values are filled in as None.

    Arguments
        G: networkx graph
        attribute: name of the node attribute in `G`
        agg: function to aggregate all of the predecessor values of `attribute`
        name: name of new attribute to be made
    Returns
        None, modifies G in place
    """
    for node in G:
        succ_res = []
        succs = G.successors(node)
        for succ in succs:
            succ_res.append((G.nodes[node][attribute] - G.nodes[succ][attribute]).days)
        if succ_res:
            G.nodes[node][name] = agg(succ_res)
        else:
            G.nodes[node][name] = None

def histplot(G, log_scale, attribute, alpha, label=None):
    res = get_node_attributes(G, attribute)
    sns.histplot(res, log_scale=log_scale, stat='density', alpha=alpha, label=label)