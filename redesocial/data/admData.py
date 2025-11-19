import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

adm_df = pd.DataFrame(columns=[
    "id",
    "name",
    "email",
    "password",
    "birthday",
    "birth_month",
    "birth_year",
    "gender",
    "status",
    "post_list",
    "tags"
])

