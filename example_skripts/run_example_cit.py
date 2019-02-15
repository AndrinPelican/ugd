import json
from test.test_resources.citation_example_graph import adj_m_cit, var_dict_citation
from ugd.high_level_interface.draw_simulations import  digraph_hyp_test

global DEBUG  # Needed to modify global copy of globvar
DEBUG = True
'''actual estimation'''
graphs, stats_list = digraph_hyp_test(adj_m=adj_m_cit, var_dict = var_dict_citation, test_variable= ('paper','B','A'), controlls=['timelayer','random'],  anz_sim=1000, show_polt=True)

