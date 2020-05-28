import copy
from ugd.schlaufen_construction.di_schlaufen_construction_util import feasible_out_nodes
from test.test_resources.graphs_two_restriction_sets import graph1
import unittest

testdata = [
    (graph1, 0, False, set([3]) ),
    (graph1, 1, True, set([0]) ),
    (graph1, 0, True, set([]) ),
]

class testFeasibleOutnodes(unittest.TestCase):

    def test_feasable_outnodes(self):

        for graph, node, is_aktive, outnodes in testdata:
            graph_copy = copy.deepcopy(graph)
            outnodes_computed = feasible_out_nodes(graph_copy, node, is_aktive)
            assert outnodes_computed == outnodes
