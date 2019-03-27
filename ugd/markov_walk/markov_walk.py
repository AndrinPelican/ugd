'''
This file is a implementation of the algorithm Markov Draw form the paper:

Uniform Sampling of Graphs with Fixed Degree Sequence under Partition Constraints

'''
import numpy as np

'''costume functions'''
from ugd.help_function.util import rand_choise
from ugd.schlaufen_construction.schlaufen import add_random_schlaufe
from ugd.markov_walk.markov_walk_util import switch_cycles, del_marks, update_violation_matrix
from ugd.markov_walk.constraint_violation_check import no_violations


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
        graph, is_violated, start_nodes, cycle_start_nodes, active_startnodes = create_schlaufen_sequence(graph)
        # switching
        if is_violated == 0:  # feasable Schlaufen sequence found
            switch_cycles(graph, cycle_start_nodes, active_startnodes)
            del_marks(graph, start_nodes)
            return graph
        else:  # self loop
            del_marks(graph, start_nodes)
            return graph


def create_schlaufen_sequence(graph):
    # finding schlaufen sequence (step 3)
    violation_matrix = np.zeros((graph.restriction_set_list.__len__(), graph.restriction_set_list.__len__()))
    ad_schlaufen = True
    start_nodes = []
    cycle_start_nodes = []
    active_cyclenodes = []

    ind = 0
    while ad_schlaufen:
        start_node, cycle_start_node, active_cyclenode = add_random_schlaufe(graph, ind)
        # fixme cycle_start says which schlaufen are of type 1, we keep trak of them determine which one to switch and return switching start nodes
        # book keeping on marked Schlaufen
        start_nodes.append(start_node)
        cycle_start_nodes.append(cycle_start_node)
        active_cyclenodes.append(active_cyclenode)
        # fixme here make list of biolation matrixes
        violation_matrix = update_violation_matrix(graph, cycle_start_node, active_cyclenode, ind, violation_matrix)

        # check feasibility of Schlaufen sequence
        # fixme here breithensuche, gibt gefundenes tupel aus oder false
        if no_violations(violation_matrix, graph):
            is_violated = False
            return graph, is_violated, start_nodes, cycle_start_nodes, active_cyclenodes
        else:
            if rand_choise(0.5):  # note feasible, random interruption
                is_violated = True
                return graph, is_violated, start_nodes, cycle_start_nodes, active_cyclenodes
        ind += 1
