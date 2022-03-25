import pandas as pd 
import sys 
import random 
from estimated_distance import estimated_distance

dataset = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

dataset = dataset.drop(columns=['variety'])

random_value = random.randint(1, 1000)*1000
name_export = "{}{}_distance_numerical.csv".format(path_export, random_value)
instance_estimator = estimated_distance(dataset, name_export)

instance_estimator.run_parallel()