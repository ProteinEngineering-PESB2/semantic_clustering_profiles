import pandas as pd
import sys
from Bio.KEGG import REST

def process_sequence(sequence_result):

    data = sequence_result.split("\n")
    description = data[0]
    sequence = "".join(value for value in data[1:] if value != "")
    return description, sequence

enzyme_list = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

matrix_data_process = []
matrix_error = []
matrix_sequence_error = []

for i in range(len(enzyme_list)):
    organism_data = enzyme_list['organism'][i]
    pathway = enzyme_list['pathway'][i]
    code_enzyme = enzyme_list['code_enzyme'][i]

    print("Processing: ", organism_data, pathway, code_enzyme)
    try:
        enzyme = REST.kegg_get(code_enzyme.lower()).read()
        enzyme = enzyme.split("\n")
        values_to_process = []

        is_filter = False
        for line in enzyme:

            if "GENE" in line:
                is_filter=True
            if "DBLINKS" in line:
                is_filter=False
            if is_filter:
                values_to_process.append(line)

        for element in values_to_process:
            values = element.split(":")
            organism = values[0].split(" ")[-1].strip().lower()
            codes = values[1].split(" ")
            codes = [code for code in codes if len(code)>1]

            for code in codes:
                value_code = code.split("(")[0]
                search = "{}:{}".format(organism, value_code)
                print("Making search: ", search)
                try:
                    #buscamos la secuencia
                    sequence = REST.kegg_get(search, option="aaseq").read()
                    description, sequence_value= process_sequence(sequence)
                    row = [organism_data, pathway, code_enzyme, search, description, sequence_value]
                    matrix_data_process.append(row)
                except:
                    row_error_seq = [organism_data, pathway, code_enzyme, search]
                    matrix_sequence_error.append(row_error_seq)
                    pass
    except:
        row_error = [organism_data, pathway, code_enzyme]
        matrix_error.append(row_error)
    break

print("Export results")
df_export = pd.DataFrame(matrix_data_process, columns=['organism', 'pathway', 'code_enzyme', 'search_data', 'desc', 'sequence'])
name_export = "{}sequences_found.csv".format(path_export)
df_export.to_csv(name_export, index=False)

df_export_error = pd.DataFrame(matrix_error, columns=['organism', 'pathway', 'code_enzyme'])
name_export = "{}sequences_found_error.csv".format(path_export)
df_export_error.to_csv(name_export, index=False)

df_export_error_2 = pd.DataFrame(matrix_error, columns=['organism', 'pathway', 'code_enzyme', 'search_id'])
name_export = "{}process_sequences_found_error.csv".format(path_export)
df_export_error_2.to_csv(name_export, index=False)
