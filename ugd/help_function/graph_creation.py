from ugd.help_function.util import form_to_set_index
from ugd.help_function.util import all_edges
from ugd.model.digraph import RstDiGraph
from ugd.model.graph import RstGraph

import numpy as np
import copy

'''
This functions generate from the input a graph in of the class defined in model.
That form is convenient and more efficient for the Schlaufen construction
'''


def generate_graph(adj_m, nodesetpartition, is_directed):
    graph = adj_m_to_graph(adj_m, is_directed)
    graph.restriction_set_list = nodesetpartition
    crossing_martix = get_crossing_matrix(graph)
    graph.crossing_matrix = crossing_martix
    graph = postprocess_graph(graph)
    return graph


def get_crossing_matrix(graph):
    crossing_matrix = np.zeros((graph.restriction_set_list.__len__(), graph.restriction_set_list.__len__()))
    edges = all_edges(graph)
    for edge in edges:
        from_ind, to_ind = form_to_set_index(graph, edge)
        if graph.is_directed:
            crossing_matrix[from_ind, to_ind] += 1
        else:
            crossing_matrix[from_ind, to_ind] += 1
            crossing_matrix[to_ind, from_ind] += 1
    return crossing_matrix


def graph_to_adj_m(graph):
    adj_m = np.zeros(shape=(graph.node_number, graph.node_number))
    for ind, node in enumerate(graph.nodes):
        for out_ind in node.outnodes:
            adj_m[ind, out_ind] += 1
    return adj_m


def adj_m_to_graph(adj_m, is_directed):
    if is_directed:
        n, indegrees, outdegrees = adj_to_in_out_sequences(adj_m)
        graph = RstDiGraph(indegree_serie=indegrees, outdegree_serie=outdegrees, restriction_set_list=None,
                           crossing_np_array=None)
        for i in range(n):
            for j in range(n):
                if adj_m[i, j] == 1:
                    graph.add_edge((i, j))
    else:
        n, degrees = adj_to_sequences(adj_m)
        graph = RstGraph(degree_serie=degrees, restriction_set_list=None, crossing_np_array=None)
        for i in range(n):
            for j in range(i, n):
                if adj_m[i, j] == 1:
                    graph.add_edge((i, j))

    return graph


def adj_to_in_out_sequences(adj):
    n = adj.shape[0]
    indegrees = []
    outdegrees = []
    for i in range(n):
        outdegrees.append(sum(adj[i, :]))
        indegrees.append(sum(adj[:, i]))
    return n, indegrees, outdegrees


def adj_to_sequences(adj):
    n = adj.shape[0]
    degrees = []
    for i in range(n):
        degrees.append(sum(adj[i, :]))
    return n, degrees


''' 
The Following function:

Updates the passive_out nodes for each node, taking out the out nodes which are not feasible because the
new node out degree 0, or a switch would imply a creation of an edge which is never in the graph. This makes 
the algorithm more efficient in handling hard constraints.

For a formal proof of correctness see:

Uniform Sampling of Graphs with Fixed Degree Sequence under Partition Constraints, Section 2.4

'''


def postprocess_graph(graph):
    for node_p in graph.nodes:
        node_p = reduce_passive_outnodes(graph, node_p)
    return graph


def reduce_passive_outnodes(graph, node_p):
    for passive_outnode in copy.deepcopy(node_p.passive_outnodes):
        if not_feasable_pas_outnode(graph, node_p.id, passive_outnode):
            node_p.passive_outnodes.remove(passive_outnode)
            node_p.passive_outnodes_removed_selfloop_crossarrow += 1
    return node_p


def not_feasable_pas_outnode(graph, node, passive_outnode):
    # chek outdegree
    if graph.is_directed:
        if graph.nodes[passive_outnode].outdegree == 0:
            return True
    else:
        if graph.nodes[passive_outnode].degree == 0:
            return True

    i, j = form_to_set_index(graph, (node, passive_outnode))
    if graph.crossing_matrix[j, i] == 0:
        return True
    return False
