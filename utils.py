import networkx as nx
import matplotlib
import pandas as pd
from networkx.algorithms import approximation
from pyvis.network import Network
from os.path import exists
import datetime
import seaborn as sns
import numpy as np

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
    """
    Graphs a sns histplot of attribute from G.

    Arguments
        G: networkx graph
        attribute: name of the node attribute in `G`
        alpha: opacity of the histplot
        label: label of graph if multiple histplots/for legend
    Returns
        None, graphs attribute from G
    """
    res = get_node_attributes(G, attribute)
    sns.histplot(res, log_scale=log_scale, stat='density', alpha=alpha, label=label)

def create_channel_graph(video_df, recommendation_df):
    """
    Creates a collapsed channel graph 

    Arguments
        video_df: df of all videos
        recommendation_df: df of all recommendations between videos
    Returns 
        Channel level multi directed edge graph
    """
    vid_to_channel = video_df[['id', 'channel_id']].rename(columns={'channel_id': 'from_channel_id'})
    vid_to_channel2 = video_df[['id', 'channel_id']].rename(columns={'channel_id': 'to_channel_id'})
    channel_to_channel = recommendation_df.merge(vid_to_channel, left_on='from_id', right_on='id').merge(vid_to_channel2, left_on='to_id', right_on='id')
    channel_to_channel = channel_to_channel[['from_channel_id', 'to_channel_id']]
    channel_to_channel
    channel_G = nx.from_pandas_edgelist(df=channel_to_channel, source="from_channel_id", target="to_channel_id", create_using=nx.MultiDiGraph)
    return channel_G

def add_channel_self_recommendation_source():
    """
    FIXME:
    Placeholder 
    """
    pass

def add_channel_self_recommendation_target():
    """
    FIXME:
    Placeholder 
    """
    pass

def jittered_scatterplot(x, y, jitter_std, alpha, s, label=None):
    """
    Graphs x and y jittered with mean 0 and std jitter_std

    Arguments
        x: x values to plot, must be same shape as y
        y: y values to plot, must be same shape as x
        jitter_std: standard deviation of the jitter 
        alpha: opacity of the histplot
        s: size of dots
        label: label of graph if multiple scatterplots/for legend
    Returns
        None, graphs jittered scatterplot
    """
    def jitter(values):
        return values + np.random.normal(0, jitter_std,values.shape)
    sns.scatterplot(x=jitter(x), y=jitter(y), alpha=alpha, s= s, label=label)
