import networkx as nx
from collections import defaultdict
import random
import matplotlib.pyplot as plt


def read_undigraph(filename):
    graph = nx.Graph()
    with open(filename, 'r') as file:
        for line in file:
            node, *edges = map(int, line.strip().split(': ')[1].split(', '))
            graph.add_edges_from((node, edge) for edge in edges)
    return graph


def read_digraph(filename):
    graph = nx.DiGraph()
    with open(filename, 'r') as file:
        for line in file:
            node, *edges = map(int, line.strip().split(': ')[1].split(', '))
            graph.add_edges_from((node, edge) for edge in edges)
    return graph


def digraph_stats(graph, name):
    print("Graph", name, end=": ")
    print("nodes:", graph.number_of_nodes(), end=", ")
    print("edges:", graph.number_of_edges())
    print("scc:", nx.number_strongly_connected_components(graph))


def undigraph_stats(graph):
    biconnect = list(nx.biconnected_components(graph))
    lens = [len(x) for x in biconnect]
    print("biggest scc:", max(lens))
    disconnect(graph, max(biconnect, key=len))


def disconnect(graph, cc):
    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    count = 0
    while temp_graph.number_of_nodes() > 0 and nx.is_connected(temp_graph):
        node_to_remove = random.choice(list(temp_graph.nodes))
        temp_graph.remove_node(node_to_remove)
        count += 1
    print("Number of random nodes till disconnect:", count, end=", ")
    print("percentage:", '{percent:.2%}'.format(
        percent=count/graph.number_of_nodes()))

    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    degrees = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    count = 0
    while temp_graph.number_of_nodes() > 0 and count < len(degrees) and nx.is_connected(temp_graph):
        node_to_remove = degrees[count][0]
        if temp_graph.has_node(node_to_remove):
            temp_graph.remove_node(node_to_remove)
        count += 1
    print("Number of highest-degree nodes till disconnect:", count)

    # temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    # betweeness = nx.betweenness_centrality(graph)
    # betweeness = sorted(betweeness.items(), key=lambda x: x[1], reverse=True)
    # count = 0
    # while count < len(degrees) and nx.is_connected(temp_graph):
    #     node_to_remove = betweeness[count][0]
    #     temp_graph.remove_node(node_to_remove)
    #     count += 1
    # print("Number of betweeness nodes till disconnect:", count)


# Example usage:
for i in range(1, 2):
    dir = 'graphs/g' + str(i) + '_directed.txt'
    undir = 'graphs/g' + str(i) + '_undirected.txt'
    digraph = read_digraph(dir)
    undigraph = read_undigraph(undir)
    digraph_stats(digraph, i)
    undigraph_stats(undigraph)
