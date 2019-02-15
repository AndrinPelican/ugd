import numpy as np

from ugd.help_function.util import graph_to_adj_m
from ugd.model.digraph import RstDiGraph

# long cycle           [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8]
indegree_serie_cit   = [0,0,0,0,0,0,0,0,0,2,0,0,1,1,2,1,1,2,0]
outdegree_serie_cit  = [0,2,0,1,0,1,3,0,0,1,2,0,0,0,0,0,0,0,0]
restriction_set_list_cit = [set([0,1,2,3,4,5,6]),set([7,8,9,10,11,12]),set([13,14,15,16,17,18])]
crossing_np_array_mr_cit = np.array(([0,3,4],[0,0,3],[0,0,0]))
graph_cit = RstDiGraph(indegree_serie_cit, outdegree_serie_cit, restriction_set_list_cit, crossing_np_array_mr_cit)

var_dict_citation = \
{
    0 : {'timelayer': 0, 'paper': 'A'},
    1 : {'timelayer': 0, 'paper': 'A'},
    2 : {'timelayer': 0, 'paper': 'A'},
    3 : {'timelayer': 0, 'paper': 'A'},
    4 : {'timelayer': 0, 'paper': 'A'},
    5 : {'timelayer': 0, 'paper': 'B'},
    6 : {'timelayer': 0, 'paper': 'B'},
    7 : {'timelayer': 1, 'paper': 'A'},
    8 : {'timelayer': 1, 'paper': 'A'},
    9 : {'timelayer': 1, 'paper': 'A'},
    10: {'timelayer': 1, 'paper': 'B'},
    11: {'timelayer': 1, 'paper': 'B'},
    12: {'timelayer': 1, 'paper': 'B'},
    13: {'timelayer': 2, 'paper': 'A'},
    14: {'timelayer': 2, 'paper': 'A'},
    15: {'timelayer': 2, 'paper': 'A'},
    16: {'timelayer': 2, 'paper': 'B'},
    17: {'timelayer': 2, 'paper': 'B'},
    18: {'timelayer': 2, 'paper': 'B'},
}

graph_cit.add_edge((1, 13))
graph_cit.add_edge((1, 16))
graph_cit.add_edge((3, 15))
graph_cit.add_edge((5, 9))
graph_cit.add_edge((6, 9))
graph_cit.add_edge((6, 17))
graph_cit.add_edge((6, 12))
graph_cit.add_edge((9, 14))
graph_cit.add_edge((10, 14))
graph_cit.add_edge((10, 17))


adj_m_cit = graph_to_adj_m(graph_cit)


