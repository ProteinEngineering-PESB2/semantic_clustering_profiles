from grafo import grafo
import numpy as np 

class adjacency_matrix(object):

    def __init__(self, dataset, dataset_distances, metric, threshold, export_name):

        self.dataset = dataset
        self.dataset_distances = dataset_distances
        self.metric = metric
        self.threshold = threshold
        self.export_name = export_name
        self.grafo_instance = grafo(metric)

    def get_nodes(self):

        print("Get nodes from list")
        list_nodes1 = [node for node in self.dataset_distances['id_1'].unique()]
        list_nodes2 = [node for node in self.dataset_distances['id_2'].unique()]

        list_nodes = list_nodes1+ list_nodes2
        list_nodes = list(set(list_nodes))

        self.grafo_instance.set_node_list(list_nodes)
    
    def get_edges(self):

        print("Get edges using define criterion: {} {}".format(self.metric, self.threshold))
        average = np.mean(self.dataset_distances[self.metric])
        std = np.std(self.dataset_distances[self.metric])
        
        list_values = [value for value in self.dataset_distances[self.metric]]
        list_values.sort()
        
        #get selected element
        total_members = int(len(list_values)*self.threshold/100)
        min_value = list_values[total_members-1]
        
        selected_data = self.dataset_distances.loc[self.dataset_distances[self.metric]<=min_value]

        edges = [[selected_data['id_1'][index], selected_data['id_2'][index], selected_data[self.metric][index]] for index in selected_data.index]

        self.grafo_instance.set_edge_list(edges)
    
    def explore_graph(self):
        self.grafo_instance.create_graph_structure()
        self.grafo_instance.community_research(self.export_name)
