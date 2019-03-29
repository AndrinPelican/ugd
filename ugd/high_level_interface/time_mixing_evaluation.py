'''
Estimates the time of the whole simulation,
estimates the average number of edges changed, in one time step (in % of totoal edges)

'''
import copy
import logging
import time

from ugd.markov_walk.markov_walk import markov_walk

logging.getLogger().setLevel(logging.INFO)


def evaluate_mixing_time(graph, mixing_time, anz_sim):
    # preparation

    edges_changed_numb = 0

    runs = 100

    # counting
    overheattime = 0
    start = time.clock()
    for i in range(runs):
        s1 = time.clock()
        compare_graph = copy.deepcopy(graph)
        e1 = time.clock()

        graph = markov_walk(graph, 1)

        s2 = time.clock()
        edges_changed_numb += edges_changed(graph, compare_graph)
        e2 = time.clock()
        overheattime += e1 - s1 + e2 - s2
        # print('run number:    ' + str(i))

    stop = time.clock()

    # validation
    if edges_changed_numb == 0:
        raise ValueError('After ' + str(
            runs) + ' runs no other graph has been found, Either there doesent exist one, or the probability of '
                    'finding one is very small and it is recommended to reconsider the problem or use '
                    'a different estimation method.')
    # completion
    n_edges = number_of_edges(graph)
    if mixing_time == None:
        mixing_time = int(10 / edges_changed_numb * runs * n_edges)

    # evaluation

    time_taken = stop - start - overheattime
    time_estimated = time_taken * anz_sim * mixing_time / runs
    edges_changed_per_draw = edges_changed_numb * mixing_time / runs / n_edges
    logging.info('The time per run is:  ' + str((time_taken / runs)) + '  seconds.')
    logging.info('The total estimation will last approximately for:  ' + str(int(time_estimated)) + '  seconds.')
    logging.info('Approximate edge changes per draw/ in percent of total edges:  ' + str(
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
