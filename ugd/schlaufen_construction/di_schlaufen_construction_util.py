from ugd.help_function.util import rand_element_of_set

''' Random draw functions:'''


def random_draw(graph, working_node, is_active):
    # draw out of feasible out node set
    out_node_set = feasible_out_nodes(graph, working_node, is_active)
    if len(out_node_set) is 0:
        return False, None
    else:
        return True, rand_element_of_set(out_node_set)


def feasible_out_nodes(graph, working_node, is_active):
    # construction of feasible out node set
    out_node_set = set([])
    if is_active:
        for out_node in graph.nodes[working_node].outnodes:
            if is_feasible_out_node(graph, working_node, out_node, is_active):
                out_node_set.add(out_node)
    else:
        for out_node in graph.nodes[working_node].passive_outnodes:
            if is_feasible_out_node(graph, working_node, out_node, is_active):
                out_node_set.add(out_node)
    return out_node_set


def is_feasible_out_node(graph, working_node, out_node, is_active):
    working_node_p = graph.nodes[working_node]
    if is_active:
        if out_node in working_node_p.outnodes and not (out_node in working_node_p.active_marked):
            return True
        else:
            return False
    else:
        if out_node in working_node_p.passive_outnodes and not (out_node in working_node_p.passive_marked) \
                and not (graph.nodes[out_node].outnodes == set([])):
            return True
        else:
            return False


''' mark functions:'''


def mark_node(graph, working_node, is_active):
    if is_active:
        graph.nodes[working_node].active_visited = True
    else:
        graph.nodes[working_node].passive_visited = True


def mark_edge(graph, working_node, out_node, is_active, schlaufen_number):
    if is_active:
        graph.nodes[working_node].active_marked[out_node] = schlaufen_number
    else:
        graph.nodes[working_node].passive_marked[out_node] = schlaufen_number


''' Control functions'''


def cycle_found(graph, out_node, is_active):
    if not is_active:  # consider that this is the new node, which is found in an is_active step but left in an
        # not is_active  step
        if graph.nodes[out_node].active_visited == True:
            return True
        else:
            return False
    else:
        if graph.nodes[out_node].passive_visited == True:
            return True
        else:
            return False
