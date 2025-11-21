import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, scrolledtext
import sys
import os
import json

# variaveis globais para as fontes
font_roboto = None
font_inter = None
font_roboto_big = None 


# paTH DO BACKEND

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
def abrir_home(usuario, font_roboto, font_inter, font_roboto_big):
    home = tk.Toplevel()
    home.title("Home")
    home.geometry("420x720")

    top = tk.Frame(home, pady=15)
    top.pack()
    tk.Label(top, text=f"Bem-vindo, {usuario}!", font=font_roboto_big).pack()

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
    tk.Label(f, text="Feed de Posts", font=font_roboto).pack(pady=10)
    feed = scrolledtext.ScrolledText(f, width=42, height=20, font=font_inter)
    feed.insert("end", "Nenhuma publicação ainda...")
    feed.configure(state="disabled")
    feed.pack()

    # Conteudo NOVO POST
    f = frames["Novo Post"]
    tk.Label(f, text="Criar Novo Post", font=font_roboto).pack(pady=10)
    post_box = scrolledtext.ScrolledText(f, width=42, height=10, font=font_inter)
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

    tk.Button(f, text="Publicar", command=publicar, width=20, height=2, font=font_inter).pack(pady=10)

    # Conteudo PROJETOS
    f = frames["Projetos"]
    tk.Label(f, text="Projetos", font=font_roboto).pack(pady=10)
    tk.Label(f, text="Projeto A\nProjeto B\nProjeto C", font=font_inter).pack()

    # Conteudo RANKING
    f = frames["Ranking"]
    tk.Label(f, text="Ranking", font=font_roboto).pack(pady=10)
    tk.Label(f, text="1. Você\n2. Usuário2\n3. Usuário3", font=font_inter).pack()

    # Conteudo PERFIL
    f = frames["Perfil"]
    tk.Label(f, text="Perfil do Usuário", font=font_roboto).pack(pady=10)
    tk.Label(f, text=f"Usuário: {usuario}", font=font_inter).pack()
    tk.Label(f, text="Bio: escreva algo sobre você", font=font_inter).pack()

    # Função para trocar abas
    def mostrar(aba):
        for fr in frames.values():
            fr.pack_forget()
        frames[aba].pack(fill="both", expand=True)

    # Barra Inferior
    barra = tk.Frame(home)
    barra.pack(side="bottom", fill="x")

    for aba in abas:
        tk.Button(barra, text=aba, width=11, font=("Inter", 10), command=lambda a=aba: mostrar(a)).pack(side="left")

    mostrar("Home")

def criar_cadastro(root, font_roboto, font_inter):
    cad = tk.Toplevel(root)
    cad.title("Cadastro")
    cad.geometry("360x500")

    tk.Label(cad, text="Criar Conta", font=font_roboto).pack(pady=20)

    tk.Label(cad, text="Usuário:", font=font_inter).pack()
    e1 = tk.Entry(cad, font=font_inter)
    e1.pack(pady=6)

    tk.Label(cad, text="Senha:", font=font_inter).pack()
    e2 = tk.Entry(cad, font=font_inter, show="*")
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

    tk.Button(cad, text="Cadastrar", width=20, height=2, command=cadastrar, font=font_inter).pack(pady=20)


#Tela de Login
def main():
    root = tk.Tk()

    
    global font_roboto, font_inter, font_roboto_big
    
    font_roboto = tkFont.Font(family="Roboto", size=14, weight="bold")
    font_roboto_big = tkFont.Font(family="Roboto", size=18, weight="bold")
    
    font_inter = tkFont.Font(family="Inter", size=12)

    root.title("Login")
    root.geometry("360x640")

    tk.Label(root, text="Login", font=font_roboto_big).pack(pady=20)

    tk.Label(root, text="Usuário:", font=font_inter).pack()
    entry_user = tk.Entry(root, font=font_inter)
    entry_user.pack(pady=6)

    tk.Label(root, text="Senha:", font=font_inter).pack()
    entry_pass = tk.Entry(root, show="*", font=font_inter)
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
        
        # 1. abre a tela principal
        abrir_home(u, font_roboto, font_inter, font_roboto_big)
        
        # 2. esconde a janela de login
        root.withdraw()

    def abrir_cadastro():
        criar_cadastro(root, font_roboto, font_inter)

    tk.Button(root, text="Entrar", width=20, height=2, command=fazer_login, font=font_inter).pack(pady=10)
    tk.Button(root, text="Criar Cadastro", width=20, height=2, command=abrir_cadastro, font=font_inter).pack()

    root.mainloop()


if __name__ == "__main__":
    main()