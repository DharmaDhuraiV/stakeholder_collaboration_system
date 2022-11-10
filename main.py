import networkx as nx
import pickle
from networkx.algorithms.bipartite import weighted_projected_graph


if __name__ == '__main__':
    with open('./dataset/data_formatted.pkl', 'rb') as file:
        data = pickle.load(file)

    graph = nx.Graph()

    graph.add_nodes_from(data['topics'], bipartite = 0)
    graph.add_nodes_from(data['projects'], bipartite = 1)
    graph.add_edges_from(data['edges'])
    
    nx.write_gexf(weighted_projected_graph(graph, [record[0] for record in data['topics']]), './Gephi/topic_projection.gexf')