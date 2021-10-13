from ugd import digraph_hyp_test
from ugd import graph_hyp_test

import numpy as np
adj_m = np.zeros((4,4))
adj_m[0,1] = 1
adj_m[2,3] = 1


ouput_dict = digraph_hyp_test(adj_m=adj_m)

print(ouput_dict["graph_list"])

