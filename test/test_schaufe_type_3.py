import numpy as np
from ugd.model.graph import RstGraph
from ugd.schlaufen_construction.schlaufen_construction import add_plain_random_schlaufe

import unittest

'''
There are only 2 graph with this restrictions for switching it the path has to go over all edges

The test idea is that if the path starts at 1 and goes to 0 then over {3,4} back to 0, then with probability 1/2
a schlaufe of type 3 is build, or the path is continued. We test whether the probability is indeed 1/2.

'''

def new_graph():
    graph = RstGraph(degree_serie=[2, 1, 1, 1, 1], restriction_set_list=[set([0]), set([1, 2]), set([3, 4])],
                     crossing_np_array=np.array(([0, 2, 0], [2, 0, 0], [0, 0, 1])))
    graph.add_edge((0, 1))
    graph.add_edge((0, 2))
    graph.add_edge((3, 4))
    return graph

class SchlaufeType3(unittest.TestCase):

    def test_schlaufe_type_3(self):
        not_case_3 = 0
        case_3 = 0

        for i in range(10000):
            graph = new_graph()

            start_node, cycle_node, active_cycle_node = add_plain_random_schlaufe(graph, schleifen_number=0)
            if start_node== 1:

                # case type 3
                if 2 in graph.nodes[0].active_marked: # the path continued to 2
                    # not case 3 at 0 link
                    not_case_3 += 1
                else:
                    if 0 in graph.nodes[3].passive_marked or  0 in graph.nodes[4].passive_marked: # the path came to 0 but didnt contunue to 2
                        case_3 += 1
        assert abs(not_case_3-case_3)/(case_3+not_case_3)<0.1