'''

This file implements the Schlaufen Detection algorithm in the paper:

Uniform Sampling of Graphs with Fixed Degree Sequence under Partition Constraints

'''

from ugd.schlaufen_construction.schlaufen_construction_util import mark_edge, mark_node, cycle_found, random_draw, is_schlaufe_type_3
from ugd.help_function.util import rand_element_of_set, del_nodes_mark


def add_plain_random_schlaufe(graph, schleifen_number):
    # random draw of initial node (step 1)
    start_node = rand_element_of_set(range(graph.node_number))

    cycle_node = None
    active_cycle_node = None
    working_node = start_node
    is_active = True
    is_schlaufe = False

    while not (is_schlaufe):


        if is_schlaufe_type_3(graph, working_node, is_active, start_node):
            is_schlaufe = True # schlaufe of type 3:

        else:

            mark_node(graph, working_node, is_active)
            found, out_node = random_draw(graph, working_node, is_active)  # step 2 or 4, depending on is_active

            if not(found):
                is_schlaufe = True  # schlaufe of type 2:
            else:
                # follow edge
                mark_edge(graph, working_node, out_node, is_active, schleifen_number)
                working_node = out_node

                if cycle_found(graph, out_node, is_active):  # step 3 or 5
                    active_cycle_node = not is_active  # out node is one step ahead
                    cycle_node = out_node
                    is_schlaufe = True # schlaufe of type 1:
                else:
                    is_active = not is_active

    del_nodes_mark(graph, start_node)  # but don't delete marked edges
    return start_node, cycle_node, active_cycle_node
