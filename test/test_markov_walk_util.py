from test.test_resources.graphs_two_restriction_sets import pathgraph1
from ugd.markov_walk.markov_walk_util import switch_cycles
import unittest


class TestMarkovWalk(unittest.TestCase):

    def test_swich_cycles(self):
        graph = switch_cycles(graph=pathgraph1, cycle_nodes= [None, 3], active_startnodes=[None, True])
        # check if (3,0 ) is in graph
        assert graph.nodes[3].outnodes == set([0])
