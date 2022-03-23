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
performance_estimator = evaluation_cluster.evaluationClustering()
unsupervised_learning_instance.applicateOptics(50, 0.05, 0.05)

print("Get performances")
performances = performance_estimator.get_metrics(dataset, unsupervised_learning_instance.labels)
print("Calinski: {}".format(performances[0]))
print("Siluetas: {}".format(performances[1]))
print("Davies: {}".format(performances[2]))
