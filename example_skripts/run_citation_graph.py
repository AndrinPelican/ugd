import json
from test.test_util.json_citation_read_in import createGraph
from ugd import digraph_hyp_test



'''loading and preparing'''
inputPaperList = json.load(open('../test/test_resources/output_24_12_17.json'))
adj_m, var_dict = createGraph(inputPaperList, [2018, 2015, 2012, 2009], 'econometric theory' )

'''actual estimation'''
graphs, stats_list = digraph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable= ('journal','econometric theory','econometric review'), controls=['timelayer', 'journal'], anz_sim=50, show_polt=True)

pass

