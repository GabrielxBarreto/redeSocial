from redesocial.views.tk_frontend import *

from redesocial.service.authService import AuthService
from redesocial.service.userService import *
from redesocial.controller.authController import *
from redesocial.model.user import User
from redesocial.data.userData import user_df 
from redesocial.data.publicationData import publication_df 
from redesocial.data.midiaData import midia_df 


import pandas as pd

#Crie o ambiente virtual antes de rodar venv(vale pro linux)
#cd documents
#source venv/bin/activate
#python3 -m redesocial.main
#a função loc do pandas df.loc[linha , coluna] é um buscador tras suporte a condições e querrys complexas
#transformar o objeto em dicionaraio antes de enviar para a tabela p.__dict__

#def main():

if __name__ == "__main__":
    main()