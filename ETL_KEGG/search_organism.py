import pandas as pd
import sys
from Bio.KEGG import REST

name_export = sys.argv[1]

print("Searching organism")
organisms = REST.kegg_list("organism").read()
organisms = organisms.split("\n")

matrix_data = []

print("Processing data")
for element in organisms:

    if len(element)>1:
        values = element.split("\t")
        values = [value.strip() for value in values]
        matrix_data.append(values)

print("Exporting results")
df_export = pd.DataFrame(matrix_data, columns=['id_code', 'code', 'name_organism', 'description'])
df_export.to_csv(name_export, index=False)


