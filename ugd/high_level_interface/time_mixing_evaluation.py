'''
Estimates the time of the whole simulation,
estimates the average number of edges changed, in one time step (in % of totoal edges)

'''
import copy
import logging
import time

from ugd.markov_walk.markov_walk import markov_walk

logging.getLogger().setLevel(logging.INFO)


def evaluate_mixing_time(graph, mixing_time, anz_sim, fast_mixing_time_evaluation):
    # preparation

    edges_changed_numb = 0

    if fast_mixing_time_evaluation:
        runs = 10
    else:
        runs = 1000

    # counting
    overheattime = 0
    start = time.time()
    for i in range(runs):
        s1 = time.time()
        compare_graph = copy.deepcopy(graph)
        e1 = time.time()

        graph = markov_walk(graph, 1)

        s2 = time.time()
        edges_changed_numb += edges_changed(graph, compare_graph)
        e2 = time.time()
        overheattime += e1 - s1 + e2 - s2
        # print('run number:    ' + str(i))

    stop = time.time()

    # validation
    if not(fast_mixing_time_evaluation) and edges_changed_numb == 0:
        raise ValueError('After ' + str(
            runs) + ' runs no other graph in the target set has been found. Either no such graph exists, or the probability of '
                    'finding one is very small. It is recommended to reconsider the problem or use '
                    'a different approach.')
    # completion
    n_edges = number_of_edges(graph)
    if mixing_time == None:
        if edges_changed_numb==0:
            logging.critical("No edges were modified while evaluating mixing time, cannot set a default mixing time. Set mixing time manually.")
        mixing_time = int(10 / edges_changed_numb * runs * n_edges)

    # evaluation

    time_taken = stop - start - overheattime
    time_per_run = time_taken / runs
    time_per_graph_creation = time_per_run * mixing_time;
    time_estimated = anz_sim * time_per_graph_creation
    edges_changed_per_draw = edges_changed_numb * mixing_time / runs / n_edges
    logging.info('Approximate time to draw one graph from the reference set                           : ' + '{:.6f}'.format(time_per_graph_creation) + ' s')
    logging.info('Total execution time is estimated at                                                : ' + str(int(time_estimated)) + ' s')
    logging.info('Approximate number of edges changed per simulated graph (as a percent of all edges) : ' + str(
        int(edges_changed_per_draw * 100)) + '%.')
    return mixing_time, edges_changed_per_draw


''' Costume functions '''


def edges_changed(graph, comparegraph):
    # counts the edges which are different between the two
    counter = 0
    for ind in range(graph.node_number):
        counter += set_difference_card(graph.nodes[ind].outnodes, comparegraph.nodes[ind].outnodes)
    return counter


def set_difference_card(set1, set2):
    # returns the number of elements in set 1 which are not in set two
    # for nodes this are the edges changed
    couter = 0
    for element in set1:
        if not (element in set2):
            couter += 1
    return couter


def number_of_edges(graph):
    counter = 0
    for node in graph.nodes:
        counter += len(node.outnodes)
    return counter
