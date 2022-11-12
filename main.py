import networkx as nx
import pickle
from rec_user import UserRecommendation
from rec_topic import topicRec


if __name__ == '__main__':
    with open('./dataset/data_formatted.pkl', 'rb') as file:
        data = pickle.load(file)

    graph = nx.Graph()

    topics = [record[0] for record in data['topics']]
    projects = [record[0] for record in data['projects']]

    graph.add_nodes_from(data['topics'], bipartite = 0)
    graph.add_nodes_from(data['projects'], bipartite = 1)
    graph.add_edges_from(data['edges'])


    rec = UserRecommendation('adrianhajdin', 'project_chat_application', graph, projects)
    neigh = rec.recommend_user()
    rec.show_graph()
    
    mgraph = nx.Graph()
    for node in neigh:
        mgraph.add_edge(rec.proj_id, node[0], weight = node[1]['weight'])

    topicRec(graph, rec.proj_id, mgraph)
    
    

