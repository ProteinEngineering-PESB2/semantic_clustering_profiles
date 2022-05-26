import pandas as pd
import sys
from Bio.KEGG import REST

dataset_pathways = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

matrix_enzyme = []
matrix_error = []

for i in range(len(dataset_pathways)):

    organism = dataset_pathways['organism'][i]
    pathway = dataset_pathways['path_id'][i]
    print("Exploring: {}, {}".format(organism, pathway))
    try:
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

        for element in values_data:
            data = element.split(";")[1].split("[")
            data = [value.replace("[", "").replace("]", "") for value in data if "EC:" in value]

            for element in data:
                values = element.split(" ")
                values = [value for value in values if len(value)>1]
                row_to_insert=""
                if len(values) == 1:
                    row_to_insert = "{};{};{}".format(organism, pathway, values[0])
                    matrix_enzyme.append(row_to_insert)
                else:
                    for value in values:
                        if "EC:" in value:
                            row_to_insert = "{};{};{}".format(organism, pathway, value)
                        else:
                            value = "EC:{}".format(value)
                            row_to_insert = "{};{};{}".format(organism, pathway, value)

                        matrix_enzyme.append(row_to_insert)
    except:
        row = [organism, pathway]
        matrix_error.append(row)

print("Filter unique data")
print(len(matrix_enzyme))
matrix_enzyme = list(set(matrix_enzyme))
print(len(matrix_enzyme))

print("Processing data to export")
matrix_to_export = [value.split(";") for value in matrix_enzyme]
ok_data = [value for value in matrix_to_export if len(value) == 3]

df_export = pd.DataFrame(ok_data, columns=['organism', 'pathway', 'code_enzyme'])
name_export = "{}enzymes_list.csv".format(path_export)
df_export.to_csv(name_export, index=False)

df_error = pd.DataFrame(matrix_error, columns=['organism', 'pathway'])
name_export = "{}enzymes_list_error.csv".format(path_export)
df_error.to_csv(name_export, index=False)
