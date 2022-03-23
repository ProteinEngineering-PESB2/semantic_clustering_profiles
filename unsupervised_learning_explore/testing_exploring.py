import sys
import pandas as pd
import force_brute_exploring

print("Get parameters and processing dataset")
#testing with iris dataset
dataset = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

#remove class response
dataset = dataset.drop(columns=['variety'])

#init instances
exploring_force = force_brute_exploring.exploring_clustering(dataset, path_export, 50, 1, 100)
exploring_force.start_exploring()