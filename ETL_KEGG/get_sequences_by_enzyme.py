import pandas as pd
import sys
from Bio.KEGG import REST

enzyme_list = pd.read_csv(sys.argv[1])
name_export = sys.argv[2]

matrix_data_process = []
matrix_error = []

