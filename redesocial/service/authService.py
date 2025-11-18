
from ..model.user import User
from ..data.userData import user_df

#df[df["nome"] == "Gabriel"]
#df[(df["idade"] > 18) & (df["cidade"] == "São Paulo")]

class AuthService:
    def login(self,user:User = None):
        if user is None:
            u = input("Informe seu Nome e senha:\nNome: ")
            p = input("Senha:")
            result = user_df[(user_df["name"] == u) & (user_df["password"] == p)]
            if not result.empty:
                user_id = result.iloc[0]["id"]
                print("Login realizado com sucesso, Bem vindo "+result.iloc[0]["name"]+"!")
                return user_id
            else:
                print("Usuário ou senha incorretos")
                return None
        else:
            print("Login realizado com sucesso, Bem vindo "+user.name+"!")
            return user.id
    def signup(self):
        print("Vamos ao cadastro:")
        name = input("Nome: ")
        email = input("Email: ")
        password = input("Senha: ")
        birthday = input("Dia do nascimento: ")
        birth_month = input("Mês do nascimento: ")
        birth_year = input("Ano do nascimento: ")
        gender = input("Gênero: ")
        satatus = 1
        post_list = []
        tags = []
        user = User(name,email,password,birthday,birth_month,birth_year,gender,satatus,post_list,tags)

        user_df.loc[len(user_df)] = user.to_dict()
        print(user_df)
        return user

        
        
        
      