import networkx as nx

class Filter:
    def __init__(self, graphNodes: dict) -> None:
        self.graphNodes = graphNodes
        self.attbr = None
        self.attbr_val = None

    def set_filter_attbr(self, attbr):
        self.attbr = attbr

    def set_filter_attbr_val(self, attbr_val):
        self.attbr_val = attbr_val
    
    def __filter(self, node):
        try:
            self.graphNodes[node][self.attbr]
        except KeyError:
            return True

        if self.attbr == 'topics':
            vals = self.attbr_val.split(',')
            attbrs = self.graphNodes[node][self.attbr].split(',')
            for val in vals:
                if val in attbrs:
                    return True
            return False

        if type(self.attbr_val) is str:
            return self.graphNodes[node][self.attbr] == self.attbr_val

        return self.graphNodes[node][self.attbr] == self.attbr_val

    def filter(self ,graph: nx.Graph):
        return nx.subgraph_view(graph, self.__filter)


# Usage
# filterObj = Filter(graph.nodes)
# filterObj.set_filter_attbr('topics')
# filterObj.set_filter_attbr_val('nodejs')
# view = filterObj.filter(graph)