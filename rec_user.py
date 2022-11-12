from Filter import Filter
import networkx as nx
import os
from uuid import uuid4
import shutil

class UserRecommendation:
    def __init__(self, username, project_name, graph, projects) -> None:
        self.username = username
        self.project_name = project_name
        self.graph = graph
        self.projects = projects

    def __get_filtered_graph(self, graph: nx.Graph, attbr:str , attbr_val):
        filter = Filter(graph.nodes)
        filter.set_filter_attbr(attbr)
        filter.set_filter_attbr_val(attbr_val)
        return filter.filter(graph)

    def recommend_user(self):
        project_projection = nx.algorithms.bipartite.weighted_projected_graph(self.graph, self.projects)

        self.projection = project_projection

        view = self.__get_filtered_graph(project_projection, 'username', self.username)
        view = self.__get_filtered_graph(view, 'repo_name', self.project_name)
        self.proj_id = list(view.nodes())[0]
        edge_list = sorted(project_projection.edges(),key=lambda edge : project_projection.edges[edge]["weight"],reverse=True)
        self.neigh_ids=[]
        
        for edge in edge_list:
            if self.proj_id==edge[0]:
                self.neigh_ids.append((edge[1], {'weight':project_projection.edges[edge]["weight"]}))
            elif self.proj_id==edge[1]:
                self.neigh_ids.append((edge[0], {'weight':project_projection.edges[edge]["weight"]}))

        return self.neigh_ids

    def show_graph(self, limit = 10):
        if limit>len(self.neigh_ids):
            limit = len(self.neigh_ids)

        graph = nx.Graph()
        for node in self.neigh_ids[:limit]:
            graph.add_edge(self.graph.nodes[self.proj_id]['username'], self.graph.nodes[node[0]]['username'], weight = node[1]['weight'])
        
        id = str(uuid4())

        os.mkdir(os.path.join(id))

        nx.write_gexf(graph, os.path.join(id, 'temp.gexf'))

        os.system('E:/Gephi-0.9.6/bin/gephi.exe -o ' + os.path.join(id, 'temp.gexf') )

        shutil.rmtree(os.path.join(id))