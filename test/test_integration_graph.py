import numpy as np
import unittest
import ugd
from test.test_resources.plain_graph_integration import adj_m_1, var_dict_1, adj_m_2, var_dict_2

class TestIntegrationGraph(unittest.TestCase):

    def test_graph_no_rstrc(self):
        output_dict= ugd.graph_hyp_test(adj_m=adj_m_1, var_dict=var_dict_1, test_variable=('gender', 'm', 'f'), mixing_time=100, anz_sim=1000, show_polt=False)
        mue = np.mean(output_dict['stat_list'])
        true_mean = 0*1/3+ 2/3 * 2 # in this simple case the true mean can be calculated manually

        true_normalized_numb_graphs_same_as_observed = 1/3
        true_quantil_with_50_50_rule = 1/6

        assert output_dict["info_dict"]["normalized_numb_graphs_same_as_observed"] > true_normalized_numb_graphs_same_as_observed - 0.15 and output_dict["info_dict"]["normalized_numb_graphs_same_as_observed"] < true_normalized_numb_graphs_same_as_observed + 0.15
        assert output_dict["info_dict"]["quantile"] > true_quantil_with_50_50_rule - 0.15 and output_dict["info_dict"]["quantile"] < true_quantil_with_50_50_rule + 0.15
        assert mue > true_mean - 0.15 and mue < true_mean + 0.15

