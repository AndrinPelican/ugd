'''

This file implements the Schlaufen Detection algorithm in the paper:

Uniform Sampling of Graphs with Fixed Degree Sequence under Partition Constraints

'''

from ugd.schlaufen_construction.schlaufen_construction_util import mark_edge, mark_node, cycle_found, random_draw
from ugd.help_function.util import rand_element_of_set, del_nodes_mark


def add_plain_random_schlaufe(graph, schleifen_number):
    # random draw of initial node (step 1)
    found_feasible_start_node = False
    while not found_feasible_start_node:  # draw start node with already a aktive outedge (smallers overhead)
        startnode = rand_element_of_set(range(graph.node_number))
        if not (graph.nodes[startnode].outnodes == set([])):
            found_feasible_start_node = True
        # fixme: write a defualt ... to avoid infinite loop

    cycle_node = None
    active_cycle_node = None
    working_node = startnode
    is_active = True
    is_schlaufe = False

    while not (is_schlaufe):
        mark_node(graph, working_node, is_active)
        found, out_node = random_draw(graph, working_node, is_active)  # step 2 or 4, depending on is_active
        if found:
            mark_edge(graph, working_node, out_node, is_active, schleifen_number)
            working_node = out_node
            if cycle_found(graph, out_node, is_active):  # step 3 or 5
                active_cycle_node = not is_active  # out node is one step ahead
                cycle_node = out_node
                is_schlaufe = True
            else:
                is_active = not is_active
        else:
            is_schlaufe = True

    del_nodes_mark(graph, startnode)  # but don't delete marked edges 
    return startnode, cycle_node, active_cycle_node
