import pandas as pd
import sys
from Bio.KEGG import REST

dataset = pd.read_csv(sys.argv[1])
name_export = sys.argv[2]

matrix_pathways = []

for i in range(len(dataset)):
    organism = dataset['code'][i]
    print("Processing organism: ", organism)
    pathways = REST.kegg_list("pathway", organism).read()

    pathways = pathways.split("\n")

    for element in pathways:
        if len(element)>1:
            element = element.split("\t")
            values = [value.strip() for value in element]
            values.insert(0, organism)
            matrix_pathways.append(values)
    
print("Exporting data")
df_export = pd.DataFrame(matrix_pathways, columns=['organism', 'path_id', 'description_path'])
df_export.to_csv(name_export, index=False)
