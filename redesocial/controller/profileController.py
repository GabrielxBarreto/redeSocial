# redesocial/controller/profileController.py

from tkinter import messagebox
# Importa o serviço de autenticação definido no seu settings.py
from ..config.settings import USER_AUTH_SERVICE 


def load_user_profile_data(username):
    """
    Carrega dados básicos e simula dados do perfil.
    Define os valores padrão para Localização, Educação e a Bio.
    """
    # 1. Busca os dados essenciais do usuário (objeto UserMock)
    user_data = USER_AUTH_SERVICE.get_user(username)
    
    if user_data:
        # 2. Retorna a estrutura de dados completa
        return {
            "username": user_data.name,
            
            # DADOS PADRÃO SOLICITADOS:
            "location": "Concórdia - SC",
            "education": "IFC Concórdia",
            
            # DADOS MOCKADOS INICIAIS (são editáveis na interface):
            "bio": "amo o alissu", # <<-- DESCRIÇÃO PADRÃO ATUALIZADA
            "interests": ["Design", "Marketing", "Fotografia"],
            
            # Posts agora é uma lista vazia, conforme solicitado
            "posts": [] 
        }
    return None

def update_user_bio(username, new_bio):
    """
    Função chamada pelo botão "Salvar Descrição" na interface.
    (Simulação de salvamento)
    """
    try:
        # ⚠️ Aqui você implementaria a lógica real de salvamento no seu DataFrame/JSON
        print(f"DEBUG: Biografia de {username} atualizada para: {new_bio}")
        messagebox.showinfo("Sucesso", "Biografia salva com sucesso!")
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar a biografia: {e}")
        return False
        
def update_user_interests(username, new_interests_list):
    """
    Função chamada ao adicionar ou remover uma tag de interesse.
    (Simulação de salvamento)
    """
    try:
        # ⚠️ Aqui você implementaria a lógica real de salvamento no seu DataFrame/JSON
        print(f"DEBUG: Interesses de {username} atualizados para: {new_interests_list}")
        messagebox.showinfo("Sucesso", "Interesses salvos com sucesso!")
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar os interesses: {e}")
        return False