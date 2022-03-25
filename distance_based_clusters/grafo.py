import networkx as nx
import pandas as pd 
import community as community_louvain

class grafo(object):
    def __init__(self, metric):
        self.metric = metric
        self.node_list = []
        self.edge_list = []

        self.partition = None
        self.modularity_value = None 
        
    def set_node_list(self, node_list):
        self.node_list = node_list
    
    def set_edge_list(self, edge_list):
        self.edge_list = edge_list
    

    def create_graph_structure(self):
        
        print("Creating graph")
        self.graph_data = nx.Graph()

        print("Adding nodes")
        for node in self.node_list:
            self.graph_data.add_node(node)

        print("Adding edges")
        for edge in self.edge_list:
            self.graph_data.add_edge(edge[0], edge[1], weigth=edge[2])
        
    def community_research(self, name_export):

        self.partition = community_louvain.best_partition(self.graph_data)
        try:
            self.modularity_value= community_louvain.modularity(self.partition, self.graph_data)
            print(self.modularity_value)
        except:
            print("Error getting modularity")
            pass

        matrix_data = []

        for data in self.partition:
            row = [data, self.partition[data]]
            matrix_data.append(row)

        dataFrame = pd.DataFrame(matrix_data, columns=["sequence", "clusterID"])
        dataFrame.to_csv(name_export, index=False)