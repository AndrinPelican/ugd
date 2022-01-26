'''
Constructs a node partition, according to the variables the user wants to control for: "controls".
The controls are keys in the variable dictionary, the node-groups (elements of the partition) are
the nodes which share the same values for all the controls.

This input from for is not a restriction, any partition can be defined via node-variables.
'''


def constr_partition(controls, var_dict, adj_m):
    if controls == None:
        nodesetpartition = [set(range(adj_m.shape[0]))]
    else:
        # fist step: create new variable out of combination of covariates
        hash_set = set([])
        for node in var_dict:
            hash_set.add(my_hash(controls, var_dict, node))

        # construct list of sets (node parition)
        nodesetpartition = []
        for place, hash in enumerate(hash_set):
            nodesetpartition.append(set([]))
            for node in var_dict:
                comp_has = my_hash(controls, var_dict, node)
                if my_hash(controls, var_dict, node) == hash:
                    nodesetpartition[place].add(node)
    return nodesetpartition


def my_hash(controls, var_dict, node):
    has_str = ''
    for control in controls:
        has_str += str(var_dict[node][control]) + '_'
    return has_str
