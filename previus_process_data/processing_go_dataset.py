import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

dataset = dataset.dropna().reset_index()
sources = dataset['source'].unique()

for source in sources:
    data = dataset.loc[dataset['source'] == source]
    print("{} : {}".format(source, len(data)))
    data = data.reset_index()

    df_export = pd.DataFrame()
    for column in ['accession','term', 'description']:
        df_export[column] = data[column]

    name_export = "{}{}_dataset.csv".format(path_export, source)
    df_export.to_csv(name_export, index=False)


