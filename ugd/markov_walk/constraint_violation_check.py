import numpy as np


''' 
no_violations checks whether all partition constraint are fulfilled.

no_violation is a interface, which can be customized. 

Examples are if you are only interested in the restriction of edges between two specific groups. In this case only the 
specific element in the matrix has to be checked.

Another example is fixing the number of triads in the graph.

'''

def no_violations(violation_matrix, graph):
    return np.all(violation_matrix==0)

