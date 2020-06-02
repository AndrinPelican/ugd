from scipy.stats import logistic
import numpy as np


def pos_weight_f(value):
    value = trim_value(value)
    return logistic.pdf(value) / logistic.cdf(value)


def neg_weight_f(value):
    value = trim_value(value)
    return logistic.pdf(value) / (1-logistic.cdf(value))

def trim_value(value):
    """
    Trims the value, so that abs(value)<20,
    Values bigger then 20 cause numerical instability when calculating logits,
    The result value dosen't change for 20 upwards
    :param value:
    :return:
    """
    if value>20:
        return 20
    if value<-20:
        return -20
    return value

def create_lcl_mst_pwf_statistic_from_thresholds(threholds_m, n, edge_util_function = None):
    """
    :param threholds_m: Thresholds_m are te thresholds per edge denoted in the paper with $t$
    :param n: number of nodes
    :param edge_util_function: function which maps a graph represented in the adjacency matrix to a matrix of the same
                               shape representing the additional utility of the agent form forming the edge
    :return:
    """
    if edge_util_function == None:
        print("Waring: No edge utility function provided, using the utility equal to the number of triads closed")
        edge_util_function = get_pot_triad_m

    # for each link
    pos_weight_m = np.zeros((n, n))
    neg_weight_m = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:  # self-loops not counted
                continue
            pos_weight_m[i, j] += pos_weight_f(threholds_m[i, j])
            neg_weight_m[i, j] += neg_weight_f(threholds_m[i, j])

    def stat(adj_m, vardict = None): # vardict is given as optional in order to be conform with the ugd API
        pot_triad_m = edge_util_function(adj_m=adj_m)  # number of triads for a link
        positive_value = np.sum(np.multiply(np.multiply(pot_triad_m, adj_m), pos_weight_m))
        neg_adj_m = clear_selfloops(1 - adj_m)
        negative_value = np.sum(np.multiply(np.multiply(pot_triad_m, neg_adj_m), neg_weight_m))
        value = positive_value - negative_value
        return value
    return stat


def get_edge_thresholds(node_dict):
    n = node_dict.__len__()

    edge_trehold_m = np.zeros((n,n))

    for i in range(n):
        for j in range(n):
            edge_trehold_m[i,j] = node_dict[i][0]+node_dict[j][1] # here in out affection determined (dimentions)
    return edge_trehold_m


def clear_selfloops(adj_m):
    for i in range(adj_m.shape[0]):
        adj_m[i,i]=0
    return adj_m


def get_pot_triad_m(adj_m):
    pot_triad_m = adj_m.dot(adj_m)
    pot_triad_m = clear_selfloops(pot_triad_m)
    return pot_triad_m


