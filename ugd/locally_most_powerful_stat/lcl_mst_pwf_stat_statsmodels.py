"""

In this function the edge probabilities under the 0-Model are estimated. These probabilities are used to calculate
the optimal test statistic.

let n be the number of nodes

Input:
    adjacency matrix: (n, n) np array
    node_dict: dictionary with same structure as in ugd
    controls: list of controls like in ugd

Output:
    Depreciated update comments

Procedure:

    1) parse the graph and node_dict into the matrix input shape for the logit model

    2) estimate the logic model

    3) predict edge probabilities

    4) reshape it into the matrix form of edge probabilities

"""
import logging
logging.getLogger().setLevel(logging.INFO)

import numpy as np
import statsmodels.api as sm
from ugd.locally_most_powerful_stat.util import create_lcl_mst_pwf_statistic_from_thresholds
from ugd.high_level_interface.construct_node_partition import constr_partition


def make_lcl_mst_pwf_stat(adj_m, var_dict=None, controls=None, edge_util_function = None):

    n = adj_m.shape[0]

    # 1) parse the graph and node_dict into the matrix input shape for the logit model
    x,y, edges_removed_due_to_sparsity = create_logit_varaibles(adj_m, var_dict, controls)

    # 2) estimate the logit probabilities
    logit_mod = sm.Logit(endog=y, exog=x)
    logit_res = logit_mod.fit(disp=True, maxiter=20)

    # in order to see whether the minimum is found and whether it is global compare the gradient, with the eigenvalues of the hessian
    logging.info(" The maximal gradient entry in found point is: "+ str(np.max(np.abs(logit_mod.score(logit_res.params)))))
    hessian = - logit_mod.hessian(logit_res.params)
    eigenvalues = np.linalg.eigvalsh(hessian)
    logging.info("Eigenvalues of Hessian: ")
    logging.info("maximal: "+ str(max(eigenvalues)) + "  minimal:   " + str(min(eigenvalues)))

    thresholds = np.dot(x,logit_res.params)
    threholds_m = logit_probs_to_matrix(thresholds,n, edges_removed_due_to_sparsity)

    # creation of the statistic
    optimal_triad_stat = create_lcl_mst_pwf_statistic_from_thresholds(threholds_m, n, edge_util_function = edge_util_function)
    return optimal_triad_stat




def create_logit_varaibles(adj_m, var_dict, controls):
    " bring the matrix shaped node varibles into a table form so that a logit package can be used to estimate"

    n = adj_m.shape[0]
    if not(var_dict is None or controls is None):
        node_set_partition = constr_partition(var_dict=var_dict, controls=controls, adj_m=adj_m)
        sort_partitition(node_set_partition )
        x = np.zeros((n * (n - 1), 2 * n + number_of_possible_crossings(node_set_partition)))
    else:
        x = np.zeros((n * (n - 1), 2 * n ))
    y = np.zeros((n * (n - 1), 1))

    k = 0
    for i in range(n):
        for j in range(n):
            if (j==i):
                continue
            else:
                # target
                y[k, 0] = adj_m[i, j]

                # affinity
                x[k, i] = 1
                x[k, n + j] = 1 # in edges are n values sifted in matrix

                # The indexes for crossing groups, all crossing from one group to another is enumerated
                if not (var_dict is None or controls is None):
                    ind = ind_of_crossing(i, j, node_set_partition)
                    x[k,2*n+ind] = 1
                k+=1

    x,y, edges_removed_due_to_sparsity = remove_sparse_edges(x,y)

    """
    Estimating the node affinity parameters is not possible because of mulitcoliniarity. Increasing
    the in affinity parameters of all nodes by the same amount as decreasing the out affinity of all parameters
    results in the same likelihood. Therefore we take out the inaffinity of the first node.
    """
    x = x[:, 1:]  # the first column is omitted due to multicoliniarity




    """
    Estimating the affinity from and to every group is not possible, 
    because of mulitcoliniarity. By adjusting the out and in affinity of all edges in one gorup
    so that within one group the affinity is the same and to the next node group edges are formed 
    more likely. (the backward edges form the other gorup can be corrected for with the group parameter
    form the other direction) 
    
    Therefore we correct for this fact by for some some parition adjancy matrix edges have
    only coeficients in one direction, such that these parition adjancy matrix edges span
    a tree over the partition graph ( therefore len(node_set_partition)-1 )
    
    due to the colums removed because of sparsity, we dont know whether the last len(node_set_partition)-1 group 
    coefficients span a tree, therefore we check iteratively whether the column is coliniar
    """
    if not(var_dict is None or controls is None):
        # due to sparsity we dont know in advance which columns we have to remove
        for i in reversed(range(x.shape[1])):
            x_reduced = np.delete(x, i, axis=1)
            if np.linalg.matrix_rank(x)==np.linalg.matrix_rank(x_reduced): # check if the colum i is collnear
                x = x_reduced

            if np.linalg.matrix_rank(x) == x.shape[1]:
                break


    # verifying whether there is multicoliniarity. This should not be the case
    if np.linalg.matrix_rank(x) < x.shape[1]:
        print("ATTENTION: the null space of x is not 0, there is multicoliniarity")

    return x,y, edges_removed_due_to_sparsity


def logit_probs_to_matrix(y, n, edges_removed_due_to_sparsity):
    """ shapes node specific values into the matrix which corresponds to the original adjacency matrix
    The two indexes original and reduced is due to the sparse edges"""

    adj_m = np.zeros([n, n])
    ind_y = 0
    ind_original = 0
    for i in range(n):
        for j in range(n):
            if (j == i):
                continue
            elif (ind_original in set(edges_removed_due_to_sparsity)):
                adj_m[i, j] = - 20
                ind_original += 1
            else:
                # target
                adj_m[i, j] = y[ind_y]
                ind_y += 1
                ind_original += 1
    return adj_m

def number_of_possible_crossings(node_set_partition):
    "for each group in partition there is one crossing to each other group "
    return len(node_set_partition)*len(node_set_partition)


def ind_of_crossing(i,j,node_set_partition):
    "enumerating all except the diagonal elements in the matrix, same principle like in create_logit_varaibles "
    k = 0
    for ind1, set1 in enumerate(node_set_partition):
        for ind2, set2 in enumerate(node_set_partition):
            if i in set1 and j in set2:
                return k
            k+=1

def remove_sparse_edges(x,y):
    """
        In sparse digraphs it often happens that an node has indegree of zero or an outdegree of zero
        or there are no edges between from one nodegroup to another.
        In this case we do not consider these "edges" because the cooeffictints of the node (or nodepartiton)
        would optimize the likeleyhood ad inifinty.

        We therefore exclude the edge and the parameter form the estimation.
        For the optimal test staistic the trasholds have to be set for each potential edge.
        The trash holds of these potential edges are set to minus infinity, so that they dont contribute
        to the teststatistic. All simulated graphs will not have an edge realisation at these potential edges
        due to the degree and the nodegrouprestrictions.
        """


    sparse_columns = []
    sparse_edges = []
    # loop over columns in order to find sparse in/out nodes or groups
    for i in range(x.shape[1]):

        column = x[:, i]
        is_sparse = True
        for j in range(x.shape[0]):
            if column[j] == 1 and y[j] == 1:
                is_sparse = False

        if is_sparse:
            sparse_columns.append(i)
            # find the corresponding edges
            for j in range(x.shape[0]):
                if column[j] == 1:
                    sparse_edges.append(j)

    sparse_edges = list(set(sparse_edges)) # remove duplicates

    # remove edges
    y = np.delete(y, sparse_edges, 0)
    x = np.delete(x, sparse_edges, 0)

    # remove the corresponding varibales
    x = np.delete(x, sparse_columns,1)

    logging.info("There are "+str(sparse_edges.__len__()) + " not considered in estimation, becaues they belong to a spares "
                                                     "node (one with no in or edge realisation at all or due to a "
                                                     "sparse group constraint")

    return x,y,sparse_edges



def sort_partitition(node_set_partition):
     """The set partition has naturally no order,
     For the sparse graph, the order can be important when deleting crossgroup varibales in order to avoid
     multicoliniarity.  This function induces a fixed order (at least in the cases where the elsments sum is unique for
     each element)"""
     node_set_partition.sort(reverse=False,  key=lambda x: sum(x))