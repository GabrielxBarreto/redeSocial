import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys
import os
import json


#paTH DO BACKEND

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.join(BASE_DIR, "redesocial")
sys.path.append(BACKEND_PATH)


try:
    from service.UserService import UserService
    user_service = UserService()
except Exception:
  
    USERS_JSON = os.path.join(BASE_DIR, "usuarios.json")

    class SimpleUserService:
        def __init__(self, path=USERS_JSON):
            self.path = path
            if not os.path.exists(self.path):
                with open(self.path, "w") as f:
                    json.dump({}, f)
            self.load()

        def load(self):
            with open(self.path, "r") as f:
                self.users = json.load(f)

        def save(self):
            with open(self.path, "w") as f:
                json.dump(self.users, f, indent=4)

        def create_user(self, username, password):
            self.load()
            if username in self.users:
                raise ValueError("Usuário já existe!")
            self.users[username] = {"password": password}
            self.save()

        def get_user(self, username):
            self.load()
            data = self.users.get(username)
            if not data:
                return None
            class U:
                def __init__(self, u, p): self.username=u; self.password=p
            return U(username, data["password"])

    user_service = SimpleUserService()


#Tela home
def abrir_home(usuario):
    home = tk.Toplevel()
    home.title("Home")
    home.geometry("420x720")

    top = tk.Frame(home, pady=15)
    top.pack()
    tk.Label(top, text=f"Bem-vindo, {usuario}!", font=("Arial", 18, "bold")).pack()

    # frames de conteudo das abas
    container = tk.Frame(home)
    container.pack(expand=True, fill="both")

    frames = {}
    abas = ["Home", "Novo Post", "Projetos", "Ranking", "Perfil"]
    for aba in abas:
        frame = tk.Frame(container)
        frames[aba] = frame

    # Conteudo da aba HOME
    f = frames["Home"]
    tk.Label(f, text="Feed de Posts", font=("Arial", 14, "bold")).pack(pady=10)
    feed = scrolledtext.ScrolledText(f, width=42, height=20)
    feed.insert("end", "Nenhuma publicação ainda...")
    feed.configure(state="disabled")
    feed.pack()

    # Conteudo NOVO POST
    f = frames["Novo Post"]
    tk.Label(f, text="Criar Novo Post", font=("Arial", 14, "bold")).pack(pady=10)
    post_box = scrolledtext.ScrolledText(f, width=42, height=10)
    post_box.pack()

    def publicar():
        texto = post_box.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite algo antes de publicar.")
            return
        feed.configure(state="normal")
        feed.insert("end", f"\n\n{usuario}: {texto}")
        feed.configure(state="disabled")
        post_box.delete("1.0", "end")
        messagebox.showinfo("OK", "Publicado!")

    tk.Button(f, text="Publicar", command=publicar, width=20, height=2).pack(pady=10)

    # Conteudo PROJETOS
    f = frames["Projetos"]
    tk.Label(f, text="Projetos", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(f, text="Projeto A\nProjeto B\nProjeto C").pack()

    # Conteudo RANKING
    f = frames["Ranking"]
    tk.Label(f, text="Ranking", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(f, text="1. Você\n2. Usuário2\n3. Usuário3").pack()

    # Conteudo PERFIL
    f = frames["Perfil"]
    tk.Label(f, text="Perfil do Usuário", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(f, text=f"Usuário: {usuario}").pack()
    tk.Label(f, text="Bio: escreva algo sobre você").pack()

    # Função para trocar abas
    def mostrar(aba):
        for fr in frames.values():
            fr.pack_forget()
        frames[aba].pack(fill="both", expand=True)

    # Barra Inferior
    barra = tk.Frame(home)
    barra.pack(side="bottom", fill="x")

    for aba in abas:
        tk.Button(barra, text=aba, width=11, command=lambda a=aba: mostrar(a)).pack(side="left")

    mostrar("Home")


#Tela de Login
def main():
    root = tk.Tk()
    root.title("Login")
    root.geometry("360x640")

    tk.Label(root, text="Login", font=("Arial", 22, "bold")).pack(pady=20)

    tk.Label(root, text="Usuário:").pack()
    entry_user = tk.Entry(root, font=("Arial", 14))
    entry_user.pack(pady=6)

    tk.Label(root, text="Senha:").pack()
    entry_pass = tk.Entry(root, show="*", font=("Arial", 14))
    entry_pass.pack(pady=6)

    def fazer_login():
        u = entry_user.get().strip()
        s = entry_pass.get().strip()

        user = user_service.get_user(u)
        if not user:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return

        if user.password != s:
            messagebox.showerror("Erro", "Senha incorreta!")
            return

        messagebox.showinfo("OK", "Login bem-sucedido!")
        abrir_home(u)

    def criar_cadastro():
        cad = tk.Toplevel(root)
        cad.title("Cadastro")
        cad.geometry("360x500")

        tk.Label(cad, text="Criar Conta", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(cad, text="Usuário:").pack()
        e1 = tk.Entry(cad, font=("Arial", 14))
        e1.pack(pady=6)

        tk.Label(cad, text="Senha:").pack()
        e2 = tk.Entry(cad, font=("Arial", 14), show="*")
        e2.pack(pady=6)

        def cadastrar():
            u = e1.get().strip()
            s = e2.get().strip()
            if not u or not s:
                messagebox.showwarning("Aviso", "Preencha tudo.")
                return
            try:
                user_service.create_user(u, s)
                messagebox.showinfo("OK", "Cadastro criado!")
                cad.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(cad, text="Cadastrar", width=20, height=2, command=cadastrar).pack(pady=20)

    tk.Button(root, text="Entrar", width=20, height=2, command=fazer_login).pack(pady=10)
    tk.Button(root, text="Criar Cadastro", width=20, height=2, command=criar_cadastro).pack()

    root.mainloop()


if __name__ == "__main__":
    main()