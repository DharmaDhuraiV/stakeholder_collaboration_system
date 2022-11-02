import networkx as nx
import pickle
from pprint import pprint

class Filter:
    def __init__(self, graphNodes: dict) -> None:
        self.graphNodes = graphNodes
        self.attbr = None
        self.attbr_val = None

    def set_filter_attbr(self, attbr):
        self.attbr = attbr

    def set_filter_attbr_val(self, attbr_val):
        self.attbr_val = attbr_val
    
    def filter(self, node):
        try:
            self.graphNodes[node][self.attbr]
        except KeyError:
            return False

        if self.attbr == 'topics':
            vals = self.attbr_val.split(',')
            attbrs = self.graphNodes[node][self.attbr].split(',')
            for val in vals:
                if val in attbrs:
                    return True
            return False

        if type(self.attbr_val) is str:
            return str(self.graphNodes[node][self.attbr]).lower() == str(self.attbr_val).lower()

        return self.graphNodes[node][self.attbr] == self.attbr_val


    
if __name__ == '__main__':
    with open('data_formatted.pkl', 'rb') as file:
        data = pickle.load(file)


    graph = nx.Graph()

    graph.add_nodes_from(data['usernames'])
    graph.add_nodes_from(data['projects'])
    graph.add_edges_from(data['edges'])
    
    filterObj = Filter(graph.nodes)
    filterObj.set_filter_attbr('stars')
    filterObj.set_filter_attbr_val(563)

    view = nx.subgraph_view(graph, filterObj.filter)

    
    for id in view.nodes():
        pprint(graph.nodes[id])
    
    # for val in view.nodes():
    #     if type(val) is not str:
    #         print('Incorrect values')
    #         exit(1)

    # nx.write_gexf(graph, '')

    # print('Filter successful')
        
        