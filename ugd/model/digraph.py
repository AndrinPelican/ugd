from ugd.model.dinode import DiNode

'''
The DiGraph contains the information on the degrees and nodes. 
The RstDiGraph contains in addition information on the restrictions (here, the number of arrows between node groups, 
or node partitions) 
'''


class DiGraph():
    def __init__(self, indegree_serie, outdegree_serie):
        self.is_directed = True
        self.indegree_serie = indegree_serie
        self.outdegree_serie = outdegree_serie
        self.node_number = outdegree_serie.__len__()
        self.nodes = []
        for i in range(indegree_serie.__len__()):
            self.nodes.append(DiNode(i, indegree_serie[i], outdegree_serie[i], self.node_number))

    def add_edge(self, edge):
        from_id, to_id = edge
        from_node = self.nodes[from_id]
        from_node.add_outarrow(to_id)
        to_node = self.nodes[to_id]
        to_node.del_passive_outarrow(from_id)

    def del_edge(self, edge):
        from_id, to_id = edge
        from_node = self.nodes[from_id]
        from_node.del_outarrow(to_id)
        to_node = self.nodes[to_id]
        to_node.add_passive_outarrow(from_id)


class RstDiGraph(DiGraph):
    # Graph extension with restriction:
    def __init__(self, indegree_serie, outdegree_serie, restriction_set_list, crossing_np_array):
        "fixed parameter"
        self.restriction_set_list = restriction_set_list  # list of the restriction subsets, disjunct nodepartition
        self.crossing_matrix = crossing_np_array

        "parameters changesed in swich search"
        # stard node nodes for schlaufen
        self.startnodes = []
        # if schlaufe constains cycle, cycle start node, otherwise 0
        self.cycle_start_nodes = []

        self.violation_matrix = None
        # build and inserted after random draw from
        super(RstDiGraph, self).__init__(indegree_serie, outdegree_serie)
