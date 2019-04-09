'''
Help function for the markov walk.
'''
import numpy as np
from ugd.help_function.util import get_path, form_to_set_index


def update_violation_matrix(graph, cycle_start_node, active_cyclenode, ind, violation_matrix):
    # counts the number of changes between/within set partition
    if cycle_start_node == None:
        return violation_matrix
    else:
        path = get_path(startnode=cycle_start_node, active_start=active_cyclenode, graph=graph, pathnumber=ind)
        is_aktive = active_cyclenode  # change, start aktie or passive depending on whether path starts with an aktiv edge
        for edge in iter_edge_in_path(path):
            violation_matrix = update_violation_matrix_by_edge(graph, violation_matrix, edge, is_aktive)
            is_aktive = not (is_aktive)
        return violation_matrix


def update_violation_matrix_by_edge(graph, violation_matrix, edge, is_active):
    # determines the changes of a single edge for the violation matrix
    from_id, to_id = form_to_set_index(graph, edge)
    if graph.is_directed:
        if is_active:
            violation_matrix[from_id, to_id] -= 1
        else:
            violation_matrix[to_id, from_id] += 1
    else:
        if is_active:
            violation_matrix[from_id, to_id] -= 1
            violation_matrix[to_id, from_id] -= 1
        else:
            violation_matrix[from_id, to_id] += 1
            violation_matrix[to_id, from_id] += 1

    return violation_matrix


def iter_edge_in_path(path):
    n = path.__len__()
    for i in range(n - 1):
        yield (path[i], path[i + 1])


def switch_cycles(graph, cycle_nodes, active_startnodes):
    for ind, cycle_node in enumerate(cycle_nodes):
        if cycle_node is None:
            continue
        else:
            is_active = active_startnodes[ind]
            path = get_path(cycle_node, is_active, graph, ind)
            for edge in iter_edge_in_path(path):
                if is_active:
                    graph.del_edge(edge)
                    is_active = not (is_active)
                else:
                    graph.add_edge((edge[1], edge[0]))
                    is_active = not (is_active)
    return graph


def del_marks(graph, start_nodes):
    for node in range(graph.node_number):
        del_outarc_marks(graph, node)
    return graph


def del_outarc_marks(graph, node):
    node_pointer = graph.nodes[node]
    node_pointer.active_marked = {}  # dictionary out_arrows as key, number of Schlaufe as Value
    node_pointer.passive_marked = {}

