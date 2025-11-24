import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

user_df = pd.DataFrame(columns=[
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
user_df.loc[len(user_df)] = {
    "id": 1,
    "name": "Gabriel",
    "email": "gabriel@example.com",
    "password": "12345",
    "birthday": 23,
    "birth_month": 7,
    "birth_year": 2006,
    "gender": "cabra macho da peste",
    "status": "active",
    "post_list": [],
    "tags": ["#python", "#dev"]
}
user_df.loc[len(user_df)] = {
    "id": 2,
    "name": "Alan",
    "email": "alan@example.com",
    "password": "12345",
    "birthday": 21,
    "birth_month": 7,
    "birth_year": 2005,
    "gender": "cabra macho da peste",
    "status": "active",
    "post_list": [],
    "tags": ["#lugar", "#dev"]
}
user_df.loc[len(user_df)] = {
    "id": 3,
    "name": "Bruno",
    "email": "bruno@example.com",
    "password": "12345",
    "birthday": 23,
    "birth_month": 7,
    "birth_year": 2006,
    "gender": "cabra macho da peste",
    "status": "active",
    "post_list": [],
    "tags": ["#python", "#dev"]
}
user_df.loc[len(user_df)] = {
    "id": 4,
    "name": "jessica",
    "email": "jessica@example.com",
    "password": "12345",
    "birthday": 23,
    "birth_month": 7,
    "birth_year": 2006,
    "gender": "cabra macho da peste",
    "status": "active",
    "post_list": [],
    "tags": ["#python", "#dev"]
}