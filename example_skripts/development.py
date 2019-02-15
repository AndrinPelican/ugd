from ugd import digraph_hyp_test
from ugd import graph_hyp_test

import numpy as np
import matplotlib.pyplot as plt
adj_m = np.zeros((4,4))
adj_m[0,1] = 1
adj_m[2,3] = 1
var_dict ={
    0: {'gender': 'm'},
    1: {'gender': 'm'},
    2: {'gender': 'f'},
    3: {'gender': 'f'},
}

adj_m_2 = np.zeros((6, 6))
adj_m_2[0, 1] = 1
adj_m_2[1, 0] = 1
adj_m_2[1, 2] = 1
adj_m_2[2, 1] = 1
adj_m_2[2, 0] = 1
adj_m_2[0, 2] = 1
adj_m_2[3, 4] = 1
adj_m_2[4, 3] = 1
adj_m_2[4, 5] = 1
adj_m_2[5, 4] = 1
adj_m_2[5, 3] = 1
adj_m_2[3, 5] = 1

var_dict_2 = {
    0: {'gender': 'm'},
    1: {'gender': 'm'},
    2: {'gender': 'f'},
    3: {'gender': 'f'},
    4: {'gender': 'f'},
    5: {'gender': 'f'},
}

out_dict = digraph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable=('gender','m','f'), mixing_time=1000, anz_sim=2, show_polt=False)

ax = out_dict['plot']
plt.show()

#out_dict = digraph_hyp_test(adj_m=adj_m, var_dict = var_dict,  mixing_time=1000, anz_sim=2, show_polt=True)

#graphs, stats_list = graph_hyp_test(adj_m=adj_m_2, var_dict = var_dict_2,  mixing_time=1000, anz_sim=100, show_polt=True)


