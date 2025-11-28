from ..model.user import User
from ..data.userData import user_df
import pandas as pd # Certifique-se de ter o pandas importado se user_df for um DataFrame

# Classe auxiliar para retornar os dados básicos que o Controller espera
class UserMock:
    """Estrutura mínima para que os Controllers (Auth e Profile)
    possam acessar o nome e a senha (e outros dados se implementados)."""
    def __init__(self, data):
        # Campos básicos para login/identificação
        self.name = data.get('name')
        self.password = data.get('password')
        # Outros campos (opcional, dependendo de quais colunas você quer expor)
        self.email = data.get('email')
        self.birthday = data.get('birthday')
        self.tags = data.get('tags')
        
class AuthService:
    
    # NOVO MÉTODO: get_user
    def get_user(self, name):
        """
        Busca um usuário pelo nome (username) no DataFrame.
        Usado pelo ProfileController.
        """
        # Filtra o DataFrame onde o nome é igual ao username
        result = user_df[(user_df["name"] == name)]
        
        if not result.empty:
            # Pega a primeira linha de resultado
            user_row = result.iloc[0]
            
            # Retorna uma instância do UserMock com os dados
            return UserMock(user_row)
        
        return None
    
    def login(self,name,password):
        
        # Filtra o DataFrame pelo nome E pela senha
        result = user_df[(user_df["name"] == name) & (user_df["password"] == password)]
        print(user_df)
        if not result.empty:
            # Retorna o objeto UserMock (ou o ID, se você preferir)
            user_id = result.iloc[0]["id"]
            user = UserMock(result.iloc[0]) # Retorna o objeto mockado
            
            print("Login realizado com sucesso, Bem vindo "+user.name+"!")
            # Retorna o objeto UserMock que tem o .name e .password (compatível com o controller)
            print("DEBUG LOGIN: ",user_id)
            return user_id
        else:
            print("Usuário ou senha incorretos")
            return None
            
    def signup(self,name,email,password,birthday,birth_month,birth_year,gender):
        

        satatus = 1
        post_list = []
        tags = []
        user = User(name,email,password,birthday,birth_month,birth_year,gender,satatus,post_list,tags)

        user_df.loc[len(user_df)] = user.to_dict()
        print(user_df)
        return user

        
        
        
      