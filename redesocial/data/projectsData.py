import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

projects_df = pd.DataFrame(columns=[
    "id",
    "title",
    "author",
    "author_id",
    "link_github",
    "description",
    "score"
    
])



import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

projects_df = pd.DataFrame([
    {
        "id": 1,
        "title": "Rede Social MIAU",
        "author": "Gabriel Barreto",
        "author_id": 1,
        "link_github": "https://github.com/GabrielxBarreto/redeSocial",
        "description": "Projeto completo de rede social feita em Tkinter, com feed, posts e sistema de login.",
        "score": 87
    },
    {
        "id": 2,
        "title": "Sistema de Chat com Sockets",
        "author": "Gabriel Barreto",
        "author_id": 1,
        "link_github": "https://github.com/GabrielxBarreto/chat-socket",
        "description": "Chat em tempo real usando Python e sockets TCP, com interface Tkinter.",
        "score": 92
    },
    {
        "id": 3,
        "title": "Algoritmos de Machine Learning",
        "author": "Gabriel Barreto",
        "author_id": 1,
        "link_github": "https://github.com/GabrielxBarreto/ml-algorithms",
        "description": "Implementações próprias de regressão linear, KNN e árvore de decisão.",
        "score": 95
    },
    {
        "id": 4,
        "title": "Sistema de Login Tkinter",
        "author": "Gabriel Barreto",
        "author_id": 1,
        "link_github": "https://github.com/GabrielxBarreto/tkinter-login",
        "description": "Tela de login moderna feita com Tkinter e integração com banco de dados.",
        "score": 81
    },
    {
        "id": 5,
        "title": "API REST em Python",
        "author": "Gabriel Barreto",
        "author_id": 1,
        "link_github": "https://github.com/GabrielxBarreto/python-api",
        "description": "API REST estruturada usando FastAPI, incluindo autenticação JWT.",
        "score": 90
    },
])
