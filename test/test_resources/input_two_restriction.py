import numpy as np

# reduction cyrcle

indegree_serie_1 =[1, 0, 1, 0]
outdegree_serie_1 =[0, 1, 0, 1]
restriction_set_list_1 =[set([0, 3]), set([1, 2])]
crossing_np_array_1 = np.array(([0, 0], [0, 0]))

# aumentation cyrcle

indegree_serie_2=[1,0,1,0]
outdegree_serie_2=[0,1,0,1]
restriction_set_list_2=[set([0,1]),set([2,3])]
crossing_np_array_2 = np.array(([0,1],[1,0]))

# long cycle
indegree_serie_3 =[0,1,0,2,0,2,0,1]
outdegree_serie_3 =[1,0,2,0,2,0,1,0]
restriction_set_list_3=[set([0,1,2,3]),set([4,5,6,7])]
crossing_np_array_3 = np.array(([0,0],[0,0]))




# impossible long
indegree_serie_4 =[2,0,2,1,1,2,0]
outdegree_serie_4=[1,1,0,3,2,0,1]
restriction_set_list_4=[set([0,1,2,3]),set([4,5,6])]
crossing_np_array_4 = np.array(([0,0],[0,0]))


# possible not equlibrated:
# long cycle
indegree_serie_5 =[0,2,1,1,1,1,1,1]
outdegree_serie_5 = [2,0,0,3,0,1,1,1]
restriction_set_list_5=[set([0,1,2,3,4]),set([5,6,7])]
crossing_np_array_5 = np.array(([0,0],[0,0]))

