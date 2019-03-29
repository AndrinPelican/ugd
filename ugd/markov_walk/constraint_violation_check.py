import numpy as np
from ugd.markov_walk.markov_walk_util import is_feasible , set_elm_to_non_exept
from itertools import combinations

''' 
no_violations checks whether all partition constraint are fulfilled.

no_violation is a interface, which can be customized. 

Examples are if you are only interested in the restriction of edges between two specific groups. In this case only the 
specific element in the matrix has to be checked.

Another example is fixing the number of triads in the graph.

'''





def fesable_switch_schlaufen_combination(violation_matrices,active_cyclenodes):

    last_ind = active_cyclenodes.__len__()-1
    # Case 1 only switch last created schlaufe, or last created schlaufe is not switchable
    if active_cyclenodes[-1]== None:
        is_feasible_bool = False
        return is_feasible_bool, 'placeholder'  # then no new switchable schlaufe has been found

    # indexes of schlaufen of type 1
    switch_ind_list = []
    for i, element in enumerate(active_cyclenodes[:-1]): # last schlaufe is alwais conidered
        if not(element is None):
            switch_ind_list.append(i)

    # search for switchable combination of violation matrices
    for i in range(0,2):
        for try_indexes in combinations(switch_ind_list,i):
            try_indexes = list(try_indexes)
            try_indexes.append(last_ind)
            subsample_violation_matrices = [violation_matrices[k] for k in try_indexes]
            if is_feasible(subsample_violation_matrices):
                is_feasible_bool = True
                switch_cycle_nodes = set_elm_to_non_exept(active_cyclenodes, try_indexes)
                return is_feasible_bool, switch_cycle_nodes


    if is_feasible(violation_matrices):
        is_feasible_bool = True
        return is_feasible_bool, active_cyclenodes


    is_feasible_bool = False
    return is_feasible_bool, 'placeholder'  # then no new switchable schlaufe has been found



