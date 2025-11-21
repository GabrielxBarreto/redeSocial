
from ..model.user import User
from ..data.userData import user_df

#df[df["nome"] == "Gabriel"]
#df[(df["idade"] > 18) & (df["cidade"] == "São Paulo")]

class AuthService:
    def login(self,name,password):
        
        result = user_df[(user_df["name"] == name) & (user_df["password"] == password)]
        if not result.empty:
            user_id = result.iloc[0]["id"]
            print("Login realizado com sucesso, Bem vindo "+result.iloc[0]["name"]+"!")
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

        
        
        
      