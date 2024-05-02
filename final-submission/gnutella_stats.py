import networkx as nx
import matplotlib.pyplot as plt
import random

# reading in data file
def read_digraph(file_path):
    graph = nx.DiGraph()
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            if line.strip() and not line.startswith('#'):
                s, t = line.strip().split('\t')
                graph.add_edge(int(s), int(t))
    return graph

# calculate strongly connected components
def scc(G):
    post_order = []
    sccs = []
    vis = set()
    # transpose the graph
    G_T = G.reverse()

    # ----------------------------------------------------------------------- #
    # dfs subroutine that calculates post order and total SCC's
    def dfs(n, opt):
        # opt: 0 -> post_order, 1 -> SCC
        stack = [n]
        scc = set()
        while stack:
            # top of stack
            c_node = stack[-1]
            vis.add(c_node)
            next_nhbr = None

            # depending on option variable
            if opt == 0:
                nhbrs = G[c_node]
            else:
                nhbrs = G_T[c_node]
                scc.add(c_node)

            for nhbr in nhbrs:
                if nhbr not in vis:
                    next_nhbr = nhbr
                    break
            if next_nhbr is not None:
                stack.append(next_nhbr)
            else:
                post_order.append(stack.pop()) if opt == 0 else stack.pop()

        if opt == 1:
            sccs.append(scc)
    # ----------------------------------------------------------------------- #
    # DFS on graph
    for n in G.nodes():
        if n not in vis:
            dfs(n, 0)
    # DFS on G_T using post-order
    vis.clear()
    while post_order:
        n = post_order.pop()
        if n not in vis:
            dfs(n, 1)
    return sccs

# create subgraph with slice ratio
def create_subgraph(graph, ratio):
    if ratio == 1:
        return graph
    bcc = scc(graph)
    bcc = sorted(bcc, key=len, reverse=True)
    k = len(bcc) // ratio
    nodes = []
    for i in range(0, k):
        nodes.extend(bcc[i])
    return graph.subgraph(nodes)

# calculate directed graph statistics
def digraph_stats(graph, name, front):
    print(front + "Graph", name, end=": ")
    print(front + "nodes:", graph.number_of_nodes(), end=", ")
    print(front + "edges:", graph.number_of_edges())
    print(front + "scc:", len(scc(graph)))

# return dictionary of average neighbor scores
def avg_nhbrs(graph):
    ret = {}
    for node in graph.nodes():
        nhbrs = list(graph.neighbors(node))
        sum = 0
        for nhbr in nhbrs:
            sum += graph.degree(nhbr)
        ret[node] = sum / len(nhbrs) if len(nhbrs) > 0 else 0
    return ret

# main robustness tests
def robustness_tests(graph, cc, front):
    print(front + "Robustness Measures:")
    avg = 0
    for _ in range(5):
        temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
        count = 0
        while temp_graph.order() > 0 and nx.is_connected(temp_graph):
            node_to_remove = random.choice(list(temp_graph.nodes))
            temp_graph.remove_node(node_to_remove)
            count += 1
        avg += count
    avg /= 5
    space = max(7-len(str(count)), 0)
    fill = space * " "
    print(front + "Random nodes till disconnect:", int(avg), end=", ")
    print(front + fill + "percentage:", '{percent:.2%}'.format(
        percent=avg/temp_graph.order()))

    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    degrees = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    count = 0
    while temp_graph.order() > 0 and count < len(degrees) and nx.is_connected(temp_graph):
        node_to_remove = degrees[count][0]
        if temp_graph.has_node(node_to_remove):
            temp_graph.remove_node(node_to_remove)
        count += 1

    space = max(5-len(str(count)), 0)
    fill = space * " "
    print(front + "High-deg nodes till disconnect:", count, end=", ")
    print(front + fill + "percentage:", '{percent:.2%}'.format(
        percent=count/temp_graph.order()))

    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    betweenness = btwn_cent(graph, k=graph.order()//10)
    betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
    count = 0
    while temp_graph.order() > 0 and count < len(betweenness) and nx.is_connected(temp_graph):
        node_to_remove = betweenness[count][0]
        if node_to_remove in temp_graph:
            temp_graph.remove_node(node_to_remove)
        count += 1

    space = max(4-len(str(count)), 0)
    fill = space * " "
    print(front + "Betweenness nodes till disconnect:", count, end=", ")
    print(front + fill + "percentage:", '{percent:.2%}'.format(
        percent=count/temp_graph.order()))

    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    nhbrs = avg_nhbrs(graph)
    nhbrs = sorted(nhbrs.items(), key=lambda x: x[1], reverse=True)
    count = 0
    while temp_graph.order() > 0 and count < len(nhbrs) and nx.is_connected(temp_graph):
        node_to_remove = nhbrs[count][0]
        if node_to_remove in temp_graph:
            temp_graph.remove_node(node_to_remove)
        count += 1

    space = max(5-len(str(count)), 0)
    fill = space * " "
    print(front + "Avg nhbr nodes till disconnect:", count, end=", ")
    print(front + fill + "percentage:", '{percent:.2%}'.format(
        percent=count/temp_graph.order()))
    # ---------------------------------------------------
    print(front + "Failure Simulation (avg 10):")
    avg = 0
    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    for _ in range(10):
        avg += seq_fail(graph, temp_graph, rand_n(temp_graph))
    print(front + "Sequential failure random: ", avg/10)
    avg = 0
    top_deg = degrees[:10]
    for i in range(10):
        avg += seq_fail(graph, temp_graph, top_deg[i][0])
    print(front + "Sequential failure high-deg: ", avg/10)
    avg = 0
    top_btw = betweenness[:10]
    for _ in range(10):
        avg += seq_fail(graph, temp_graph, top_btw[i][0])
    print(front + "Sequential failure betweenness: ", avg/10)
    avg = 0
    top_nhbr = nhbrs[:10]
    for _ in range(10):
        avg += seq_fail(graph, temp_graph, top_nhbr[i][0])
    print(front + "Sequential failure avg nhbr: ", avg/10)
    print(front + "Network Repair Types (avg 10):")
    avg = 0
    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    for _ in range(10):
        for _ in range(50):
            edge_add_rand(temp_graph)
        avg += seq_fail(graph, temp_graph, rand_n(temp_graph))
    # ---------------------------------------------------
    print(front + "Seq fail rand after 50 added: ", avg/10)
    avg = 0
    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    for _ in range(10):
        for _ in range(50):
            edge_add(temp_graph, dict(graph.degree()))
        avg += seq_fail(graph, temp_graph, top_deg[i][0])
    print(front + "Seq fail high-deg after 50 added: ", avg/10)
    avg = 0
    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    for _ in range(10):
        for _ in range(50):
            edge_add(temp_graph, dict(betweenness))
        avg += seq_fail(graph, temp_graph, top_btw[i][0])
    print(front + "Seq fail betweenness after 50 added: ", avg/10)
    avg = 0
    temp_graph = nx.induced_subgraph(graph, [x for x in cc]).copy()
    for _ in range(10):
        for _ in range(50):
            edge_add(temp_graph,  dict(graph.degree()))
        avg += seq_fail(graph, temp_graph, top_nhbr[i][0])
    print(front + "Seq fail avg nhbr after 50 added: ", avg/10)

# sequential failure routine
def seq_fail(graph, cc, s):
    temp_graph = cc.copy()
    count = 0
    queue = [s]
    while temp_graph.order() > 0 and queue and nx.is_connected(temp_graph):
        nhbrs = graph.neighbors(queue[0])
        node = queue.pop(0)
        if node in temp_graph:
            temp_graph.remove_node(node)
            count += 1
        queue.extend(nhbrs)
    return count

# between centrality calculation
def btwn_cent(graph, k):
    ret = {node: 0 for node in graph}
    count = 0
    for node in graph:
        if count > k:
            break
        stack = []
        predecessors = {node: [] for node in graph}
        sigma = {node: 0 for node in graph}
        sigma[node] = 1
        dist = {node: -1 for node in graph}
        dist[node] = 0

        queue = [node]
        while queue:
            current_node = queue.pop(0)
            stack.append(current_node)
            for nhbr in graph[current_node]:
                if dist[nhbr] < 0:
                    queue.append(nhbr)
                    dist[nhbr] = dist[current_node] + 1
                if dist[nhbr] == dist[current_node] + 1:
                    sigma[nhbr] += sigma[current_node]
                    predecessors[nhbr].append(current_node)

        delta = {node: 0 for node in graph}
        while stack:
            current_node = stack.pop()
            for predecessor in predecessors[current_node]:
                delta[predecessor] += (sigma[predecessor] /
                                       sigma[current_node]) * (1 + delta[current_node])
            if current_node != node:
                ret[current_node] += delta[current_node]
        count += 1

    n = len(graph)
    normalization_factor = (n - 1) * (n - 2) / 2
    for node in ret:
        ret[node] /= normalization_factor

    return ret

# add random edge 
def edge_add_rand(graph):
    nodes = list(graph.nodes())
    random.shuffle(nodes)
    node1, node2 = nodes[:2]
    if not graph.has_edge(node1, node2):
        graph.add_edge(node1, node2)
    else:
        edge_add_rand(graph)

# add edge by metric
def edge_add(graph, metric):
    total_val = sum(metric.values())
    probabilities = {node: degree / total_val for node,
                     degree in metric.items()}

    node1 = random.choices(list(probabilities.keys()),
                           weights=list(probabilities.values()))[0]
    node2 = random.choices(list(probabilities.keys()),
                           weights=list(probabilities.values()))[0]

    if not graph.has_edge(node1, node2):
        graph.add_edge(node1, node2)
    else:
        edge_add(graph, metric)

# return random node from graph
def rand_n(graph):
    return random.choice(list(graph.nodes()))

# driver function for testing robustness
def tests(graph, front):
    biconnect = list(nx.biconnected_components(graph))
    robustness_tests(graph, max(biconnect, key=len), front)

# main function
for i in range(4, 7):
    dir = 'p2p-Gnutella0' + str(i) + '.txt'
    digraph = read_digraph(dir)
    undigraph = digraph.to_undirected()
    digraph_stats(digraph, i, "")
    for j in range(1, 5):
        subgraph = create_subgraph(digraph, round(j))
        digraph_stats(subgraph, str(
            i) + " {:.0f}".format(100 * subgraph.order()/digraph.order()) + "%", "  ")
        tests(subgraph.to_undirected(), "    ")
