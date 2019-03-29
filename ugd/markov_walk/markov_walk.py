'''
This file is a implementation of the algorithm Markov Draw form the paper:

Uniform Sampling of Graphs with Fixed Degree Sequence under Partition Constraints

'''
import numpy as np

'''costume functions'''
from ugd.help_function.util import rand_choise
from ugd.schlaufen_construction.schlaufen import add_random_schlaufe
from ugd.markov_walk.markov_walk_util import switch_cycles, del_marks, get_violation_matrix
from ugd.markov_walk.constraint_violation_check import fesable_switch_schlaufen_combination
from ugd.help_function.controll_functions_graph import full_graph_correct

def markov_walk(graph, mixing_time):
    '''
    :param graph: RstDiGraph or RstGraph class
    :param mixing_time: integer
    :return: randomly modified  RstDiGraph or RstGraph class, if mixing time is sufficiency big it is a uniform sample
    '''

    # loop over random alteration (step 1-4, in the paper)
    for i in range(mixing_time):
        graph = do_random_step(graph)
    return graph


def do_random_step(graph):
    q = 0.05
    if rand_choise(q):  # self loop (step 2)
        return graph
    else:
        graph, is_feasible, start_nodes, switch_cycle_nodes, active_startnodes = create_schlaufen_sequence(graph)
        # switching
        if is_feasible:  # feasable Schlaufen sequence found
            switch_cycles(graph, switch_cycle_nodes, active_startnodes)
            del_marks(graph, start_nodes)

            return graph
        else:  # self loop
            del_marks(graph, start_nodes)
            return graph


def create_schlaufen_sequence(graph):
    # finding schlaufen sequence (step 3)
    ad_schlaufen = True
    start_nodes = []
    cycle_start_nodes = []
    active_cyclenodes = []
    violation_matrixes = []

    ind = 0
    while ad_schlaufen:
        start_node, cycle_start_node, active_cyclenode = add_random_schlaufe(graph, ind)
        # book keeping on marked Schlaufen
        start_nodes.append(start_node)
        cycle_start_nodes.append(cycle_start_node)
        active_cyclenodes.append(active_cyclenode)
        violation_matrixes.append(get_violation_matrix(graph, cycle_start_node, active_cyclenode, ind))

        # find a feasibel combination of Schlaufen
        is_feasible , switch_cycle_nodes = fesable_switch_schlaufen_combination(violation_matrixes, cycle_start_nodes)
        if is_feasible:
            return graph, is_feasible, start_nodes, switch_cycle_nodes, active_cyclenodes
        else:
            if rand_choise(0.1):  # note feasible, random interruption
                return graph, is_feasible, start_nodes, switch_cycle_nodes, active_cyclenodes
        ind += 1

