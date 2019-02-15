'''
Control functions:
Performing checks on the Graph, to see whether implicit restrictions (double arrow, degree  ect) are fulfilled.
Checks whether there are no contradicting graph data saved (in case of redundancy)
'''

import numpy as np
from ugd.help_function.util import all_edges, form_to_set_index

'GRAPH:'


def graph_correct(graph):
    restriction(graph)
    graph_nodes_correct(graph)
    return True


def full_graph_correct(graph):
    restriction(graph)
    graph_nodes_correct(graph)
    graph_is_full(graph)
    matrix_consistent(graph)
    return True


def graph_nodes_correct(graph):
    node_id_in_place(graph)
    for node in graph.nodes:
        node_correct(node, graph.node_number)
    return True


def restriction(rstrGraph):
    # checks whether partition input is correct (disjoint partition of integers {0,..,n-1}
    set_list = rstrGraph.restriction_set_list
    total_Set = set()
    total = 0
    for sub_set in set_list:
        total_Set = total_Set.union(sub_set)
        total += sub_set.__len__()
    if not (total == total_Set.__len__()):
        raise ValueError('restriction sets are not disjoint')
    if not (total_Set == set(range(rstrGraph.degree_serie.__len__()))):
        raise ValueError('nodes in set are not the integers {0,..n-1}')


def graph_is_full(graph):
    # checks whether the graph degrees are consistent with the degree sequence
    for i, node in enumerate(graph.nodes):
        if not (graph.degree_serie[i] == node.degree):
            raise ValueError('indegree property not fulfielled')
        if not (graph.degree_serie[i] == node.outnodes.__len__()):
            raise ValueError('indegree property not fulfielled')


def matrix_consistent(rstGraph):
    # controls whether the graph fulfills the partition restriction
    n = rstGraph.restriction_set_list.__len__()
    controll_matrix = np.zeros((n, n))
    for edge in all_edges(rstGraph):
        from_ind, to_ind = form_to_set_index(rstGraph, edge)
        controll_matrix[from_ind, to_ind] += 1
        controll_matrix[to_ind, from_ind] += 1
    if not (controll_matrix == rstGraph.crossing_matrix).all():
        raise ValueError('Graph has the partition restrictions violated')


'NODE:'


def node_id_in_place(graph):
    for i, node in enumerate(graph.nodes):
        if not (i == node.id):
            raise ValueError('id and node position does not match')


def node_correct(node, n):
    if not (node.degree == node.outnodes.__len__()):
        raise ValueError(' degree violated !!')
    if not (node.degree == n - node.passive_outnodes.__len__() - node.passive_outnodes_removed_selfloop_crossarrow):
        raise ValueError(' passive out nodes number incorrect (considering hard constraints)!!')

    for outnode in node.outnodes:
        if outnode == node.id:
            raise ValueError('self loop')
        if outnode in node.passive_outnodes:
            raise ValueError('active out node is in possible passive out nodes')
