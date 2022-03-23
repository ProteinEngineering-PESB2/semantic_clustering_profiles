import selecting_best_partitions
import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])

selection = selecting_best_partitions.selection_process(dataset, [], 1.5, 1.5)
response = selection.get_statistics_values_by_performance(["calinski_haraabasz", "siluetas", "davis"])

print(response)

selection.select_best_calinski_siluetas("calinski_haraabasz")
selection.select_best_calinski_siluetas("siluetas")