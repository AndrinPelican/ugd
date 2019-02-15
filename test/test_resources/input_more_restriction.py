from copy import deepcopy

import numpy as np

from ugd.model import RstGraph

# long cycle
indegree_serie_mr_0 = [1,1,1]
outdegree_serie_mr_0 =[1,1,1]
restriction_set_list_mr_0 = [set([0]),set([1]),set([2])]
crossing_np_array_mr_0 = np.array(([0,1,0],[0,0,1],[1,0,0]))
graph_mr_0_emty = RstGraph(indegree_serie_mr_0, outdegree_serie_mr_0,restriction_set_list_mr_0,crossing_np_array_mr_0 )



# long cycle
indegree_serie_mr_1 = [1,1,1,1,1,1]
outdegree_serie_mr_1 =[1,1,1,1,1,1]
restriction_set_list_mr_1 = [set([0,1]),set([2,3]),set([4,5])]
crossing_np_array_mr_1 = np.array(([0,1,0],[0,0,1],[1,0,0]))

graph_mr_1_emty = RstGraph(indegree_serie_mr_1, outdegree_serie_mr_1,restriction_set_list_mr_1,crossing_np_array_mr_1 )
graph_mr_1 = RstGraph(indegree_serie_mr_1, outdegree_serie_mr_1,restriction_set_list_mr_1,crossing_np_array_mr_1 )
graph_mr_1.add_edge((5,0))
graph_mr_1.add_edge((0,2))
graph_mr_1.add_edge((2,3))
graph_mr_1.add_edge((3,1))
graph_mr_1.add_edge((1,4))
graph_mr_1.add_edge((4,5))
graph_mr_1.update_crossing_surplus_array()

graph_mr_2 = deepcopy(graph_mr_1_emty)
graph_mr_2.add_edge((5,0))
graph_mr_2.add_edge((0,2))
graph_mr_2.add_edge((2,3))
graph_mr_2.add_edge((3,5))
graph_mr_2.add_edge((1,4))
graph_mr_2.add_edge((4,1))
graph_mr_2.working_node = 5
graph_mr_2.fixed_to_nodes = set([0])
graph_mr_2.update_crossing_surplus_array()