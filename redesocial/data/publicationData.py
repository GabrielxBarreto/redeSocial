import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

publication_df = pd.DataFrame(columns=[
    "id",
    "type",
    "midia_list",
    "description",
    "user",
    "day",
    "times"
])
publication_df.loc[len(publication_df)] = {
    "id": 1,
    "type": "text",
    "midia_list": [],
    "description": "Gabriel publicou um novo post!",
    "user": 1,
    "day": "2025-11-23",
    "times": "14:35:12"
}
publication_df.loc[len(publication_df)] = {
    "id": 2,
    "type": "text",
    "midia_list": [],
    "description": "alan publicou um novo post!",
    "user": 1,
    "day": "2025-11-23",
    "times": "14:35:12"
}
publication_df.loc[len(publication_df)] = {
    "id": 3,
    "type": "text",
    "midia_list": [],
    "description": "bruno publicou um novo post!",
    "user": 1,
    "day": "2025-11-23",
    "times": "14:35:12"
}

publication_df.loc[len(publication_df)] = {
    "id": 1,
    "type": "text",
    "midia_list": [],
    "description": "Gabriel publicou um novo post!",
    "user": 1,
    "day": "2025-11-23",
    "times": "14:35:12"
}

publication_df.loc[len(publication_df)] = {
    "id": 4,
    "type": "text",
    "midia_list": [],
    "description": "jessica publicou um novo post!",
    "user": 1,
    "day": "2025-11-23",
    "times": "14:35:12"
}

