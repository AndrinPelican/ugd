from ugd.help_function.util import rand_element_of_set
import numpy as np

''' Random draw functions:'''

def is_schlaufe_type_3(graph, working_node, is_active, start_node):
    if working_node==start_node:
        return False # the startnode cannot close a schlaufe of type 3, because there is initially no edge leading to it

    # when it is already marked it must be an odd cycle, because otherwise a schlaufe of type I would have been returned
    if graph.nodes[working_node].active_visited or graph.nodes[working_node].passive_visited:
        return random_schlaufe_of_type_3(graph, working_node, is_active)
    return False

def random_schlaufe_of_type_3(graph, working_node, is_active):
    # gives with probability 1/ # (feasible_outnodes+1) True out else false
    outnodes_number = feasible_out_nodes(graph, working_node, is_active).__len__()

    return np.random.choice([True,False],1, p=[1/(outnodes_number+1), 1-1/(outnodes_number+1)])


def random_draw(graph, working_node, is_active):
    # draw out of feasible out nodset
    out_node_set = feasible_out_nodes(graph, working_node, is_active)
    if len(out_node_set) is 0:
        return False, None
    else:
        return True, rand_element_of_set(out_node_set)


def feasible_out_nodes(graph, wokingnode, is_active):
    # construction of feasible out node set
    out_node_set = set([])
    if is_active:
        for out_node in graph.nodes[wokingnode].outnodes:
            if is_feasible_out_node(graph, wokingnode, out_node, is_active):
                out_node_set.add(out_node)
    else:
        for out_node in graph.nodes[wokingnode].passive_outnodes:
            if is_feasible_out_node(graph, wokingnode, out_node, is_active):
                out_node_set.add(out_node)
    return out_node_set


def is_feasible_out_node(graph, working_node, out_node, is_active):
    working_node_p = graph.nodes[working_node]
    out_node_p = graph.nodes[out_node]
    if is_active:
        if out_node in working_node_p.outnodes and not (out_node in working_node_p.active_marked) \
                and not (working_node in out_node_p.active_marked):
            return True
        else:
            return False
    else:
        if out_node in working_node_p.passive_outnodes and not (out_node in working_node_p.passive_marked) \
                and not (working_node in out_node_p.passive_marked) and not (graph.nodes[out_node].outnodes == set([])):
            return True
        else:
            return False


''' mark functions:'''


def mark_node(graph, working_node, is_active):
    if is_active:
        graph.nodes[working_node].active_visited = True
    else:
        graph.nodes[working_node].passive_visited = True


def mark_edge(graph, working_node, out_node, is_active, schleifennumber):
    if is_active:
        graph.nodes[working_node].active_marked[out_node] = schleifennumber
    else:
        graph.nodes[working_node].passive_marked[out_node] = schleifennumber


''' Control functions'''


def cycle_found(graph, out_node, is_active):
    if not is_active:  # consider that this is the new node, which is found in an is_active step but left in
        # an not(is_active) step
        if graph.nodes[out_node].active_visited == True:
            return True
        else:
            return False
    else:
        if graph.nodes[out_node].passive_visited == True:
            return True
        else:
            return False

