import tkinter as tk
from tkinter import messagebox
from ..service.authService import AuthService

#Adicionar Função para ir direto!!!

def loginController(root,entry_name=None,entry_password=None):
    label_result = tk.Label(root, text="", font=("Arial", 12))
    label_result.pack()
    service = AuthService()
    if entry_name is not None and entry_password is not None: 
        name = entry_name.get()
        password = entry_password.get()
        result = service.login(name,password)
        if result is None:
            messagebox.showerror("Erro","Falhouuuu") 
            label_result.config(text="Login falhou!", fg="red")
        else:
            messagebox.showinfo("OK", "Deu certo!!!") 
            label_result.config(text="Bem-vindo!", fg="green")
    else:
        name = entry_name
        password = entry_password
        result = service.login(name,password)
        if result is None:
            messagebox.showerror("Erro","Falhouuuu") 
            label_result.config(text="Login falhou!", fg="red")
        else:
            messagebox.showinfo("OK", "Deu certo!!!") 
            label_result.config(text="Bem-vindo!", fg="green")

def signupController(entry_name,entry_email,entry_password,entry_day,entry_month,entry_year,entry_gender):
    service = AuthService()
    u = service.signup(entry_name.get(),entry_email.get(),entry_password.get(),entry_day.get(),entry_month.get(),entry_year.get(),entry_gender.get())
    loginController(u.name,u.password)

#root = tk.Tk()
#root.title("Login")
#
#tk.Label(root, text="Name").pack()
#entry_name = tk.Entry(root)
#entry_name.pack()
#
#tk.Label(root, text="Password").pack()
#entry_password = tk.Entry(root, show="*")
#entry_password.pack()
#
#btn = tk.Button(root, text="Entrar", command=lambda:loginController(entry_name,entry_password))
#btn.pack(pady=10)
#
#label_result = tk.Label(root, text="", font=("Arial", 12))
#label_result.pack()
#
## --- CAMPOS DO FORMULÁRIO ---
#
#tk.Label(root, text="Nome:").pack(anchor="w")
#entry_name = tk.Entry(root)
#entry_name.pack(fill="x")
#
#tk.Label(root, text="Email:").pack(anchor="w")
#entry_email = tk.Entry(root)
#entry_email.pack(fill="x")
#
#tk.Label(root, text="Senha:").pack(anchor="w")
#entry_password = tk.Entry(root, show="*")
#entry_password.pack(fill="x")
#
#tk.Label(root, text="Dia de nascimento:").pack(anchor="w")
#entry_day = tk.Entry(root)
#entry_day.pack(fill="x")
#
#tk.Label(root, text="Mês de nascimento:").pack(anchor="w")
#entry_month = tk.Entry(root)
#entry_month.pack(fill="x")
#
#tk.Label(root, text="Ano de nascimento:").pack(anchor="w")
#entry_year = tk.Entry(root)
#entry_year.pack(fill="x")
#
#tk.Label(root, text="Gênero:").pack(anchor="w")
#entry_gender = tk.Entry(root)
#entry_gender.pack(fill="x")
#
#
#tk.Button(root, text="Cadastrar", command=lambda:signupController(entry_name,entry_email,entry_password,entry_day,entry_month,entry_year,entry_gender)).pack(pady=20)
#
#root.mainloop()