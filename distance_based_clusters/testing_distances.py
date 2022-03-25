import pandas as pd 
import sys 
import random 
from estimated_distance import estimated_distance

dataset = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

#remove response
dataset = dataset.drop(columns=['variety'])

dataset['id'] = [i+1 for i in range(len(dataset))]

random_value = random.randint(1, 1000)*1000
name_export = "{}{}_distance_numerical.csv".format(path_export, random_value)
name_export_dataset = "{}{}_processed_dataset.csv".format(path_export, random_value)

instance_estimator = estimated_distance(dataset, name_export)

instance_estimator.run_parallel()

dataset.to_csv(name_export_dataset, index=False)