from test.test_resources.nyakatoke_data.nyakatoke_network import di_adj_m, var_dict
import numpy as np

from ugd import digraph_hyp_test
from ugd.help_function.graph_creation import adj_to_in_out_sequences, generate_graph, get_crossing_matrix
from ugd.high_level_interface.construct_node_partition import constr_partition


anz_sim = 3

# wealth and religion is unrelated nearly

def test_assert_crossingmatrix():
    di_adj_m1 =di_adj_m
    out_dict = digraph_hyp_test(adj_m=di_adj_m,var_dict=var_dict,test_variable=('wealth','rich','poor'),anz_sim=anz_sim, show_polt=False, controls=['wealth'])
    partition = constr_partition(controls =['wealth'], var_dict= var_dict, adj_m=di_adj_m)

    di_adj_m2 = out_dict['graph_list'][anz_sim - 1]
    _, ins1, outs1 = adj_to_in_out_sequences(di_adj_m1)
    _, ins2, outs2 = adj_to_in_out_sequences(di_adj_m2)

    crossing_matrix1 = generate_graph(di_adj_m1, partition, is_directed=True).crossing_matrix
    crossing_matrix2 = generate_graph(di_adj_m2, partition, is_directed=True).crossing_matrix
    assert np.array_equal(crossing_matrix1, crossing_matrix2) and np.array_equal(ins1, ins2)

