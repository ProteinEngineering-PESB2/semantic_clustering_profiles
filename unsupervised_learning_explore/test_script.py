import classical_ml_clustering
import evaluation_cluster
import pandas as pd
import sys

print("Get parameters and processing dataset")
#testing with iris dataset
dataset = pd.read_csv(sys.argv[1])

#remove class response
dataset = dataset.drop(columns=['variety'])

print("Apply some example clustering")
unsupervised_learning_instance = classical_ml_clustering.aplicateClustering(dataset)
unsupervised_learning_instance.aplicateAffinityPropagation()

print("Get performances")
performance_estimator = evaluation_cluster.evaluationClustering(dataset, unsupervised_learning_instance.labels)
print("Calinski: {}".format(performance_estimator.calinski))
print("Siluetas: {}".format(performance_estimator.siluetas))
print("Davies: {}".format(performance_estimator.davies))
