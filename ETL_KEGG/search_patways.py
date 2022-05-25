import pandas as pd
import sys
from Bio.KEGG import REST

dataset = pd.read_csv(sys.argv[1])
name_export = sys.argv[2]

matrix_pathways = []
code_error_list = []

for i in range(len(dataset)):
    organism = dataset['code'][i]
    print("Processing organism: ", organism)

    try:
        pathways = REST.kegg_list("pathway", organism).read()

        pathways = pathways.split("\n")

        for element in pathways:
            if len(element)>1:
                element = element.split("\t")
                values = [value.strip() for value in element]
                values.insert(0, organism)
                matrix_pathways.append(values)
    except:
        code_error_list.append(organism)
    break

print("Exporting data")
df_export = pd.DataFrame(matrix_pathways, columns=['organism', 'path_id', 'description_path'])
df_export.to_csv(name_export, index=False)

df_error = pd.DataFrame()
df_error['organism_error'] = code_error_list
df_error.to_csv("error_list_organism_found_pathwats.csv", index=False)