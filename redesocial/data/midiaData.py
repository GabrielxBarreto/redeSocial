import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

midia_df = pd.DataFrame(columns=[
    "id",
    "type",
    "size",
    "name",
    "original_path",
    "id_user",
    "id_publication"
])