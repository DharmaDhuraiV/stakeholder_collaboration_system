import networkx as nx
import os
from uuid import uuid4
import shutil

def topicRec(graph: nx.Graph, project, view_proj: nx.Graph, limit = 10):
    simiProjList = view_proj.neighbors(project)
    proj1topics = graph.neighbors(project)
    print(list(proj1topics))
    
    dis_similar_proj = {} # key = topic, value = weight of simiProj(if more than one getting average) 

    weight = nx.get_edge_attributes(view_proj, "weight")

    for simiProj in simiProjList:
        for topic in graph.neighbors(simiProj):
            if topic not in proj1topics:
                if topic in dis_similar_proj:
                    dis_similar_proj[topic] += weight[project, simiProj]

                dis_similar_proj[topic] = weight[project, simiProj]

    rec_topics_list = sorted(list(dis_similar_proj.items()), key = lambda n : graph.degree(n[0])*n[1],reverse=True)

    if limit>len(rec_topics_list):
        limit = len(rec_topics_list)
    
    topic_rec = [record[0] for record in rec_topics_list[:limit]]

    graph_topics = nx.Graph()

    weight = len(topic_rec)
    for node in topic_rec:
        graph_topics.add_edge(graph.nodes[project]['username'], node, weight = weight)
        weight-=1
    
    id = str(uuid4())
    os.mkdir(os.path.join(id))

    nx.write_gexf(graph_topics, os.path.join(id, 'temp.gexf'))

    os.system('E:/Gephi-0.9.6/bin/gephi.exe -o ' + os.path.join(id, 'temp.gexf'))

    shutil.rmtree(os.path.join(id))
    
    return 

