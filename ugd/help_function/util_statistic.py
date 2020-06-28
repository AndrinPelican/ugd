'''
Utility functions for statistic:
Graph statistic and evaluation of quartiles.
'''

import numpy as np
from ugd.help_function.util import check_symmetric


def get_quantile(true_val, sim_values):
    numb_lower = 0
    for value in sim_values:
        if value < true_val:
            numb_lower += 1
        if value == true_val:
            numb_lower += 0.5
    quant = numb_lower / sim_values.__len__()
    return quant

def get_normalized_numb_graphs_same_as_observed(true_val, sim_values):
    numb_same = 0
    for value in sim_values:
        if value == true_val:
            numb_same += 1
    normalized_numb_graphs_same_as_observed = numb_same / sim_values.__len__()
    return normalized_numb_graphs_same_as_observed


def get_default_stat(adj_m):
    # reciprocity statistic count number of bidirectional arrows (for directed networks)
    def reciprocity(adj_m, var_dict):
        return np.trace(adj_m.dot(adj_m)) / 2

    # transitivity statistic count number triads for a undirected network
    def transitivity(adj_m, var_dict):
        return np.trace(adj_m.dot(adj_m.dot(adj_m))) / 3 / 2 # /2 due to both direction of the triad

    # decide which one to return:
    if check_symmetric(adj_m):
        return transitivity
    else:
        return reciprocity


def crossarrow_count(adj_m, var_dict, test_border):
    key, from_value, to_value = test_border
    count = 0;
    n = adj_m.shape[0]
    for i in range(n):
        for j in range(n):
            if adj_m[i, j] == 1 and var_dict[i][key] == from_value and var_dict[j][key] == to_value:
                count += 1
    return count
