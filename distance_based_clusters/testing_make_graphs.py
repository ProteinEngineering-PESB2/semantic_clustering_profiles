import pandas as pd 
import sys 

from make_adjacency_matrix import adjacency_matrix

dataset_processed = pd.read_csv(sys.argv[1])
dataset_distances = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

random_value = sys.argv[1].split("/")[-1].split("_")[0]
metrics = ["euclidean", "cosine"]

for metric in metrics:

    name_export = "{}{}_{}_community_test.csv".format(path_output, random_value, metric)
    print(name_export)
    graph_creator = adjacency_matrix(dataset_processed, dataset_distances, metric, 25, name_export)
    graph_creator.get_nodes()
    graph_creator.get_edges()
    graph_creator.explore_graph()
