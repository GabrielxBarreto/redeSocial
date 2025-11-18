import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

publication_df = pd.DataFrame(columns=[
    "id",
    "type",
    "midia_list",
    "description",
    "user"
])