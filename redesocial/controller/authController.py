# redesocial/controller/authController.py

import tkinter as tk
from tkinter import messagebox

# Importa o serviço e o objeto de serviço
from ..config.settings import USER_AUTH_SERVICE

# Importa a View que será aberta
from ..views.home_view import abrir_home

def loginController(root, entry_name=None, entry_password=None):
    
    if isinstance(entry_name, tk.Entry) and isinstance(entry_password, tk.Entry):
        name = entry_name.get().strip()
        password = entry_password.get().strip()
        
        # Ignora placeholders
        if name == "Seu e-mail": name = ""
        if password == "Sua senha": password = ""
        
    else:
        name = entry_name
        password = entry_password

    if not name or not password:
        messagebox.showwarning("Aviso", "Preencha usuário e senha.")
        return

    # Chama o método login do service
    result = USER_AUTH_SERVICE.login(name, password)

    if result is None:
        messagebox.showerror("Erro", "Login Falhou!")
    else:
        messagebox.showinfo("OK", "Login bem-sucedido!")
        
        # Abre a tela Home e esconde a tela de Login
        abrir_home(name, root) 
        root.withdraw()


def signupController(root, entry_name, entry_email, entry_password, entry_day, entry_month, entry_year, entry_gender):
    
    try:
        # Chama o método signup do service (ele faz a validação e salva)
        user_obj = USER_AUTH_SERVICE.signup(
            entry_name.get().strip(),
            entry_email.get().strip(),
            entry_password.get().strip(),
            entry_day.get().strip(),
            entry_month.get().strip(),
            entry_year.get().strip(),
            entry_gender.get().strip()
        )
        
        if user_obj:
            messagebox.showinfo("OK", "Cadastro concluído. Acessando...")
            # Faz login automático
            loginController(root, user_obj.name, user_obj.password)
        
    except ValueError as e:
        messagebox.showerror("Erro de Cadastro", str(e))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro desconhecido: {e}")