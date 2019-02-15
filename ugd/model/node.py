class Node():
    '''
    The DiNode class is specifically designed for altering path search.

    -  Active and passive out nodes, for easily iteratively find new nodes in path.
    -  Marks for easy look up edges already visited (earlier Schlaufen) / nodes in path-creation already visited
    -  The edge-marks have the Schlaufen number saved, such that later a reconstruction of the Schlaufen found is
       possible
    '''

    def __init__(self, id, degree, totalnodes):
        self.id = id
        self.degree = degree

        self.passive_outnodes = set(range(totalnodes))
        self.passive_outnodes.remove(id)
        self.passive_outnodes_removed_selfloop_crossarrow = 1  # for graph correctness check
        self.outnodes = set()

        # marks
        self.active_visited = False
        self.passive_visited = False

        # marked edges
        self.active_marked = {}  # dictionary outarrows as key, number of schlaufe as Value
        self.passive_marked = {}

    def add_outedge(self, out_node):
        self.outnodes.add(out_node)

    def add_passive_outedge(self, out_node):
        self.passive_outnodes.add(out_node)

    def del_outedge(self, out_node):
        if not (out_node in self.outnodes):
            raise ValueError('outnode subtraction error')
        else:
            self.outnodes.remove(out_node)

    def del_passive_outedge(self, out_node):
        if not (out_node in self.passive_outnodes):
            raise ValueError('outnode subtraction error')
        else:
            self.passive_outnodes.remove(out_node)
