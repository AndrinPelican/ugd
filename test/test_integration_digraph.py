import numpy as np
import pytest
import unittest



import ugd
from test.test_resources.graphs_two_restriction_sets import graph1_adj_m, graph2_adj_m, var_dict2

var_dict1 = {
    0: {'gender': 'm', 'age': 50},
    1: {'gender': 'm', 'age': 50},
    2: {'gender': 'f', 'age': 51},
    3: {'gender': 'f', 'age': 51},
}

class TestIntegrationCrossingMatrix(unittest.TestCase):

    def test_graph_no_rstrc(self):
        output_dict= ugd.digraph_hyp_test(adj_m=graph1_adj_m, var_dict=var_dict1, test_variable=('gender', 'm', 'f'),
                                              anz_sim=1000, mixing_time=100 , show_polt=False)
        stats_list = output_dict['stat_list']
        mue = np.mean(stats_list)
        assert mue > 0.45 and mue < 5.5


    def teste_graph_with_rstrc(self):
        with pytest.raises(ValueError):
            _ = ugd.digraph_hyp_test(adj_m=graph1_adj_m, var_dict=var_dict1, test_variable=('gender', 'm', 'f'),
                                 anz_sim=1000, controls=['age'])


    def test_graph2_with_rstrc(self):
        output_dict = ugd.digraph_hyp_test(adj_m=graph2_adj_m, var_dict=var_dict2, test_variable=('gender', 'm', 'f'),
                                              anz_sim=1000)
        stats_list = output_dict['stat_list']
        mue = np.mean(stats_list)
        assert mue > 0.33333-0.05 and mue < 0.33333+0.05

    def test_graph2_no_rstrc(self):
         output_dict = ugd.digraph_hyp_test(adj_m=graph2_adj_m, var_dict=var_dict2, test_variable=('gender', 'm', 'f'),
                                        anz_sim=1000, controls=['age'])
         stats_list = output_dict['stat_list']
         mue = np.mean(stats_list)
         assert mue > 0.45 and mue < 5.5



