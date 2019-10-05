'''
Validates the user input, to check whether the API requirements are fulfilled and whether the input graph is correct.
It there is a violation it throws an error with a hint what is violated.
Depending on the input, the default parameters are substituted.
'''

import numpy as np
from ugd.high_level_interface.construct_node_partition import constr_partition
from ugd.help_function.util_statistic import get_default_stat, crossarrow_count
import warnings

''' Validation '''


def validate_input(adj_m, anz_sim, mixing_time, var_dict, stat_f, controlls, test_variable, is_directed):
    # throws error if violated
    adj_m = validate_adj_matrix(adj_m, is_directed)
    anz_sim = validate_pos_int(anz_sim)
    if not (mixing_time == None):
        mixing_time = validate_pos_int(mixing_time)
    var_dict = validate_var_dict(var_dict, adj_m.shape[0])
    stat_f = validate_stat_f(stat_f, adj_m=adj_m, var_dict=var_dict)
    controlls = validate_controls(controlls, var_dict)
    test_variable = validate_test_variable(test_variable, var_dict)


def validate_adj_matrix(adj_m, is_directed):
    if not (isinstance(adj_m, np.ndarray)):
        raise ValueError("Adjacency matrix must be a numpy array.")

    n = adj_m.shape[0]
    if not (adj_m.shape[0] == adj_m.shape[1]):
        ValueError('Adjacency matrix must be quadratic (n x n).')

    for i in range(n):
        for j in range(n):
            if not (adj_m[i, j] == 0) and not (adj_m[i, j] == 1):
                raise ValueError('Matrix is only allowed to have 0, 1 entries (no double arrow).')

            if not (is_directed):  # the plain graph case
                if not (adj_m[j, i] == adj_m[i, j]):
                    raise ValueError('For plain graph adjacency matrix must be symmetric.')
    if adj_m.sum() == 0:
        raise ValueError('Adjacency matrix must have at least one nonzero entry, empty graph not allowed.')

    for i in range(n):
        if adj_m[i, i] == 1:
            raise ValueError('Diagonal entries of matrix must be 0, (no self loops).')
    return adj_m


def validate_pos_int(anz_sim):
    try:
        anz_sim = int(anz_sim)
    except ValueError:
        print("anz_sim must be an integer.")
    if anz_sim <= 0:
        raise ValueError("anz_sim must be positive.")
    return anz_sim


def validate_var_dict(var_dict, n):
    if var_dict == None:
        return True
    if not (isinstance(var_dict, dict)):
        raise ValueError("var_dict must be a dictionary.")

    if not (n == var_dict.__len__()):
        raise ValueError(
            'var_dict must be a dictionary with primary key the integer 1..n, where n is the number of nodes.')

    for i in range(n):
        if not (i in var_dict):
            raise ValueError(
                'var_dict must be a dictionary with primary key the integer 1..n, where n is the the number of nodes.')
        if not (isinstance(var_dict[i], dict)):
            raise ValueError(
                "Values of var_dict must be a dictionary, with the variable name as key and the variable value as value")
    return var_dict


def validate_stat_f(stat_f, adj_m, var_dict):
    if not (stat_f == None):
        try:
            a = stat_f(adj_m, var_dict)
            try:
                b = int(a)
            except:
                raise ValueError('stat_f must be a function of form stat_f(adj_m, var_dict), and return a number.')
        except:
            raise ValueError('stat_f must be a function of form stat_f(adj_m, var_dict), and return a number.')
    return stat_f


def validate_controls(controls, var_dict):
    if controls == None:
        return controls
    if not (isinstance(controls, list)):
        raise ValueError('controls must be a list of variable names.')
    for i in range(var_dict.__len__()):  # see whether the controls are present in all the values of the var_dict
        for control in controls:
            if not (control in var_dict[i]):
                raise ValueError(
                    'controls must be a list of variable names, the variable names key in the all the values of var_dict \n'
                    'controls[i] in var_dict[i], for i in {0,..,n-1}')
    return controls


def validate_test_variable(test_variable, var_dict):
    if test_variable == None:
        return test_variable

    if not (isinstance(test_variable, tuple)):
        raise ValueError(' test_variable must be a tuple with 3 entries, \n'
                         ' first variable name of interest \n'
                         ' second: value of the variable form which the arrow depart \n'
                         ' third: value of the variable go which the arrow go \n'
                         )
    first_entry = False
    second_entry = False
    for i in range(var_dict.__len__()):
        if not (test_variable[0] in var_dict[i]):
            raise ValueError('test_variable must be a tuple with 3 entries, \n' +
                             'first:   variable name of interest \n' +
                             'second:  value of the variable from which the link depart \n' +
                             'third:   value of the variable go which the link go \n' +
                             'The variable name was not in the variable dict of node ', i)

        # Verify whether there are nodes with the values to test for
        if (test_variable[1] == var_dict[i][test_variable[0]]):
            first_entry = True
        if (test_variable[2] == var_dict[i][test_variable[0]]):
            second_entry = True
    if not (first_entry):
        raise ValueError('There are no nodes with the value: ', test_variable[1],
                         ' which is on the first place in the test tuple')
    if not (second_entry):
        raise ValueError('There are no nodes with the value: ', test_variable[2],
                         ' which is on the second place in the test tuple')
    return test_variable


def validate_nodesetpartition(nodesetpartition, n):
    if not (isinstance(nodesetpartition, list)):
        raise ValueError(" node partiton must be a list of sets")
    for nodest in nodesetpartition:
        if not (isinstance(nodest, set)):
            raise ValueError(" node partiton must be a list of sets")
    set_list = nodesetpartition
    total_Set = set()
    total = 0
    for sub_set in set_list:
        total_Set = total_Set.union(sub_set)
        total += sub_set.__len__()
    if not (total == total_Set.__len__()):
        raise ValueError('restriction sets are not disjoint')
    if not (total_Set == set(range(n))):
        raise ValueError('nodes in set are not the integers {0,..n-1}')
    return nodesetpartition


''' Substitution '''


def parse_input(stat_f, test_variable, controlls, var_dict, adj_m):
    # substitution input (which can be of different shape into standard shape
    if not (stat_f == None) and not (test_variable == None):
        warnings.warn('test_variable and stat_f where given, only stat_f is evaluated')
    # input substitution
    if stat_f == None:
        stat_f = get_default_stat(adj_m=adj_m)
        if not (test_variable == None):
            def crossarrow_stat(adj_m, v_dict):
                return crossarrow_count(adj_m, v_dict, test_variable)

            stat_f = crossarrow_stat

    # creation of set partition
    nodesetpartition = constr_partition(controls=controlls, var_dict=var_dict, adj_m=adj_m)
    validate_nodesetpartition(nodesetpartition, adj_m.shape[0])
    return stat_f, nodesetpartition
