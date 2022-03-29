import pandas as pd
import sys
import force_brute_exploring
import selecting_best_partitions
import os

dataset = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]
name_dir = sys.argv[3]

word_list = dataset['word']
dataset = dataset.drop(columns=['word'])

index_label =[i for i in range(len(dataset))]

command = "mkdir {}{}".format(path_export, name_dir)
print(command)
os.system(command)

path_export = "{}{}\\".format(path_export, name_dir)
exploring_force = force_brute_exploring.exploring_clustering(dataset, path_export, 20, 10, 100, index_label)
exploring_force.start_exploring()

selection = selecting_best_partitions.selection_process(exploring_force.df_explore_to_export, [], 1.5, 3)
response = selection.get_statistics_values_by_performance(["calinski_haraabasz", "siluetas", "davis"])

print(response)

selection.select_best_calinski_siluetas("calinski_haraabasz")
selection.select_best_calinski_siluetas("siluetas")
selection.select_best_davis("davis")

selection.evaluate_selection_process(["calinski_haraabasz", "siluetas", "davis"])
selection.select_partitions_by_performances(["calinski_haraabasz", "siluetas", "davis"], path_export)