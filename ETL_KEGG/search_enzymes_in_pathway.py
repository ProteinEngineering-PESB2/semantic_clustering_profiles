import pandas as pd
import sys
from Bio.KEGG import REST

dataset_pathways = pd.read_csv(sys.argv[1])
name_export = sys.argv[2]

matrix_enzyme = []

for i in range(len(dataset_pathways)):

    organism = dataset_pathways['organism'][i]
    pathway = dataset_pathways['path_id'][i]

    print("Exploring: {}, {}".format(organism, pathway))
    path = REST.kegg_get(pathway).read()

    path_result = path.split("\n")
    is_filter = False

    values_data = []

    for element in path_result:

        if 'GENE' in element:
            is_filter = True
        if 'COMPOUND' in element:
            is_filter = False
        
        if is_filter:
            values_data.append(element)
    
    #lista de genes identificados
    for value in values_data:
        data = value.split("[")[-1].replace("]", "").split(" ")
        
        for element in data:
            if "EC" not in element:
                element = "EC:{}".format(element)
            row_to_insert = "{};{};{}".format(organism, pathway, element)
            matrix_enzyme.append(row_to_insert)

print("Filter unique data")
print(len(matrix_enzyme))
matrix_enzyme = list(set(matrix_enzyme))
print(len(matrix_enzyme))

print("Processing data to export")
matrix_to_export = [value.split(";") for value in matrix_enzyme]
df_export = pd.DataFrame(matrix_to_export, columns=['organism', 'pathway', 'code_enzyme'])
df_export.to_csv(name_export, index=False)
