import numpy as np
import copy
from ugd.help_function.graph_creation import graph_to_adj_m
from ugd.help_function.control_functions_digraph import graph_correct
from ugd.model.digraph import RstDiGraph
from ugd.schlaufen_construction.di_schlaufen_construction_util import mark_edge

# reduction cyrcle
graph1 = RstDiGraph(indegree_serie=[1, 0, 1, 0], outdegree_serie=[0, 1, 0, 1], restriction_set_list=[set([0, 3]), set([1, 2])], crossing_np_array = np.array(([0, 0], [0, 0])))
graph1.add_edge((1, 0))
graph1.add_edge((3, 2))

graph1_adj_m = graph_to_adj_m(graph1)

pathgraph1 = copy.deepcopy(graph1)
mark_edge(pathgraph1, 3, 2, True, 1)
mark_edge(pathgraph1, 2, 1, False, 1)
mark_edge(pathgraph1, 1, 0, True, 1)
mark_edge(pathgraph1, 0, 3, False, 1)






##
# aumentation cyrcle
graph2 = RstDiGraph(indegree_serie=[0, 1, 0, 1, 0, 1], outdegree_serie=[1, 0, 1, 0, 1, 0], restriction_set_list=[set([0, 1, 2]), set([3, 4, 5])], crossing_np_array = np.array(([1, 1], [0, 1])))
graph2.add_edge((0,1))
graph2.add_edge((2,5))
graph2.add_edge((4,3))

var_dict2 = {
    0: {'gender': 'm', 'age': 50},
    1: {'gender': 'f', 'age': 50},
    2: {'gender': 'z', 'age': 50},
    3: {'gender': 'z', 'age': 51},
    4: {'gender': 'z', 'age': 51},
    5: {'gender': 'z', 'age': 51},
}

graph2_adj_m =graph_to_adj_m(graph2)


# long cycle
indegree_serie =[0,1,0,2,0,2,0,1]
outdegree_serie=[1,0,2,0,2,0,1,0]
restriction_set_list=[set([0,1,2,3]),set([4,5,6,7])]
crossing_np_array = np.array(([0,0],[0,0]))
graph3 = RstDiGraph(indegree_serie, outdegree_serie, restriction_set_list, crossing_np_array)
graph3emty = RstDiGraph(indegree_serie, outdegree_serie, restriction_set_list, crossing_np_array)

graph3.add_edge((0,1))
graph3.add_edge((2,3))
graph3.add_edge((2,5))
graph3.add_edge((4,3))
graph3.add_edge((4,5))
graph3.add_edge((6,7))
graph_correct(graph3)

# impossible long
indegree_serie =[2,0,2,1,1,2,0]
outdegree_serie=[1,1,0,3,2,0,1]
restriction_set_list=[set([0,1,2,3]),set([4,5,6])]
crossing_np_array = np.array(([0,0],[0,0]))
graph4 = RstDiGraph(indegree_serie, outdegree_serie, restriction_set_list, crossing_np_array)
graph4emty = RstDiGraph(indegree_serie, outdegree_serie, restriction_set_list, crossing_np_array)
graph4.add_edge((1,0))
graph4.add_edge((0,2))
graph4.add_edge((3,0))
graph4.add_edge((3,2))
graph4.add_edge((3,4))
graph4.add_edge((4,3))
graph4.add_edge((4,5))
graph4.add_edge((6,5))
graph_correct(graph4)

# possible not equlibrated:
# long cycle
indegree_serie =[0,2,1,1,1,1,1,1]
outdegree_serie=[2,0,0,3,0,1,1,1]
restriction_set_list=[set([0,1,2,3,4]),set([5,6,7])]
crossing_np_array = np.array(([0,0],[0,0]))
graph5 = RstDiGraph(indegree_serie, outdegree_serie, restriction_set_list, crossing_np_array)
graph5emty = RstDiGraph(indegree_serie, outdegree_serie, restriction_set_list, crossing_np_array)
graph5.add_edge((0,1))
graph5.add_edge((0,2))
graph5.add_edge((3,1))
graph5.add_edge((3,4))
graph5.add_edge((3,5))
graph5.add_edge((5,3))
graph5.add_edge((6,7))
graph5.add_edge((7,6))
graph_correct(graph5)
