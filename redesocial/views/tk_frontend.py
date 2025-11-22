import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, scrolledtext
from ..controller.authController import loginController
from ..controller.authController import  signupController

import sys
import os
import json
from PIL import Image, ImageTk 

# variaveis globais para as fontes
font_roboto = None
font_inter = None
font_roboto_big = None 

# CORES PARA DARK MODE
dark_theme_colors = {
    "bg_main": "#F0F0F0",       
    "fg_text": "#1E1E1E",        
    "bg_frame": "#E8E8E8",      
    "bg_button": "#505050",     
    "fg_button": "#FFFFFF",      
    "bg_entry": "#FFFFFF",      
    "fg_entry": "#1E1E1E",       
    "border": "#CCCCCC",         
    "active_bg_button": "#6A6A6A", 
    "placeholder_fg": "#A0A0A0", 
    "purple_button": "#4B0082", 

    # CORES DA BARRA INFERIOR 
    "bottom_bar_bg": "#1E1E1E",  
    "icon_inactive_fg": "#8A2BE2", 
    "icon_active_fg": "#E6E6FA", 
    "button_bar_bg": "#1E1E1E"   
}


# paTH DO BACKEND E CAMINHOS
VIEWS_DIR = os.path.dirname(os.path.abspath(__file__)) 
BASE_DIR = os.path.dirname(VIEWS_DIR) 
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


# ficao para carregar icons
def carregar_icone(nome_arquivo, tamanho=None):
    path = os.path.join(VIEWS_DIR, "img", nome_arquivo) 
    try:
        img_pil = Image.open(path)
       
        if nome_arquivo.endswith(".png") and tamanho: 
          
            img_pil = img_pil.resize(tamanho) 
        return ImageTk.PhotoImage(img_pil)
    except FileNotFoundError:
        print(f"AVISO: Ícone não encontrado em {path}. Usando apenas texto/botão padrão.")
        return None
    except Exception as e:
        print(f"AVISO: Erro ao processar ícone {nome_arquivo}: {e}")
        return None


def on_entry_click(event, entry_widget, placeholder_text):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")
        entry_widget.config(fg=dark_theme_colors["fg_entry"])

def on_focus_out(event, entry_widget, placeholder_text):
    if entry_widget.get() == "":
        entry_widget.insert(0, placeholder_text)
        entry_widget.config(fg=dark_theme_colors["placeholder_fg"])


#Tela home
def abrir_home(usuario, font_roboto, font_inter, font_roboto_big, login_root): 
    home = tk.Toplevel(bg=dark_theme_colors["bg_main"]) 
    home.title("Home")
    home.geometry("420x720")

    
    tamanho_icone = (30, 30) 
    icones = {
        "Home": carregar_icone("home_image.png", tamanho=tamanho_icone),
        "Novo Post": carregar_icone("newpost_image.png", tamanho=tamanho_icone),
        "Projetos": carregar_icone("projeto_image.png", tamanho=tamanho_icone), 
        "Ranking": carregar_icone("ranking_image.png", tamanho=tamanho_icone),
        "Perfil": carregar_icone("user_image.png", tamanho=tamanho_icone) 
    }
   
    
    # lista de buttons da barra para manipulação posterior
    botoes_barra = []
    
    # Função de Logout 
    def fazer_logout():
        home.destroy()      
        login_root.deiconify() 
        messagebox.showinfo("Logout", "Sessão encerrada com sucesso.")

    # Frame superior
    top = tk.Frame(home, pady=15, bg=dark_theme_colors["bg_main"]) 
    top.pack()
    tk.Label(top, text=f"Bem-vindo, {usuario}!", font=font_roboto_big, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack()

    # frames de conteudo das abas
    container = tk.Frame(home, bg=dark_theme_colors["bg_main"])
    container.pack(expand=True, fill="both")

    frames = {}
    abas = ["Home", "Novo Post", "Projetos", "Ranking", "Perfil"]
    for aba in abas:
        frame = tk.Frame(container, bg=dark_theme_colors["bg_frame"]) 
        frames[aba] = frame

    # Conteúdo das abas (MANTIDO)
  
    
    # Conteudo da aba HOME
    f = frames["Home"]
    tk.Label(f, text="Feed de Posts", font=font_roboto, 
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack(pady=10)
    feed = scrolledtext.ScrolledText(f, width=42, height=20, font=font_inter,
                                      bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                                      insertbackground=dark_theme_colors["fg_entry"]) 
    feed.insert("end", "Nenhuma publicação ainda...")
    feed.configure(state="disabled")
    feed.pack()

    # Conteudo NOVO POST
    f = frames["Novo Post"]
    tk.Label(f, text="Criar Novo Post", font=font_roboto, 
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack(pady=10)
    post_box = scrolledtext.ScrolledText(f, width=42, height=10, font=font_inter,
                                          bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                                          insertbackground=dark_theme_colors["fg_entry"])
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

    tk.Button(f, text="Publicar", command=publicar, width=20, height=2, font=font_inter,
              bg=dark_theme_colors["bg_button"], fg=dark_theme_colors["fg_button"],
              activebackground=dark_theme_colors["active_bg_button"], activeforeground=dark_theme_colors["fg_button"]).pack(pady=10)

    # Conteudo PROJETOS
    f = frames["Projetos"]
    tk.Label(f, text="Projetos", font=font_roboto, 
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack(pady=10)
    tk.Label(f, text="Projeto A\nProjeto B\nProjeto C", font=font_inter,
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack()

    # Conteudo RANKING
    f = frames["Ranking"]
    tk.Label(f, text="Ranking", font=font_roboto, 
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack(pady=10)
    tk.Label(f, text="1. Você\n2. Usuário2\n3. Usuário3", font=font_inter,
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack()

    # Conteudo PERFIL
    f = frames["Perfil"]
    tk.Label(f, text="Perfil do Usuário", font=font_roboto, 
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack(pady=10)
    tk.Label(f, text=f"Usuário: {usuario}", font=font_inter,
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack()
    tk.Label(f, text="Bio: escreva algo sobre você", font=font_inter,
             bg=dark_theme_colors["bg_frame"], fg=dark_theme_colors["fg_text"]).pack()
    
    # button de logout adicionado
    tk.Button(f, text="Logout", command=fazer_logout, font=font_inter,
              bg=dark_theme_colors["bg_button"], fg=dark_theme_colors["fg_button"],
              activebackground=dark_theme_colors["active_bg_button"], activeforeground=dark_theme_colors["fg_button"]).pack(pady=30)
    

   
    def mostrar(aba):
        for fr in frames.values():
            fr.pack_forget()
        frames[aba].pack(fill="both", expand=True)
        
     
        for btn in botoes_barra:
            if btn.cget("text") == aba:
                
                btn.config(fg=dark_theme_colors["icon_active_fg"], 
                           activeforeground=dark_theme_colors["icon_active_fg"])
            else:
               
                btn.config(fg=dark_theme_colors["icon_inactive_fg"], 
                           activeforeground=dark_theme_colors["icon_inactive_fg"])

   
    
    barra_frame = tk.Frame(home, bg=dark_theme_colors["bg_main"])
    barra_frame.pack(side="bottom", fill="x", padx=0)
    
   
    barra = tk.Frame(barra_frame, bg=dark_theme_colors["bottom_bar_bg"], 
                     height=60, relief="flat", bd=0, padx=5, pady=5) 
    barra.pack(fill="x")


    for aba in abas:
        icone = icones.get(aba)
        
        
        initial_fg = dark_theme_colors["icon_active_fg"] if aba == "Home" else dark_theme_colors["icon_inactive_fg"]
        
        btn = tk.Button(
            barra, 
            text=aba, 
            image=icone, 
            compound='top', 
            width=60, 
            command=lambda a=aba: mostrar(a),
            font=("Inter", 9),
            bd=0, 
            highlightthickness=0,
            # Cores da barra
            bg=dark_theme_colors["button_bar_bg"], 
            fg=initial_fg, 
            activebackground=dark_theme_colors["bottom_bar_bg"], 
            activeforeground=initial_fg 
        )
        btn.pack(side="left", expand=True, fill="x", padx=5)
        botoes_barra.append(btn) 
   

    # Refs
    home.icon_refs = list(icones.values()) 
    
    mostrar("Home") 

# funçcao de criar cadastro
def criar_cadastro(root, font_roboto, font_inter, img_cadastrar_confirm):
    cad = tk.Toplevel(root, bg=dark_theme_colors["bg_main"]) 
    cad.title("Cadastro")
    cad.geometry("360x500")

    tk.Label(cad, text="Criar Conta", font=font_roboto, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack(pady=20)

    tk.Label(cad, text="Usuário:", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack()
    e1 = tk.Entry(cad, font=font_inter,
                  bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                  insertbackground=dark_theme_colors["fg_entry"])
    e1.pack(pady=6)

    tk.Label(cad, text="Senha:", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack()
    e2 = tk.Entry(cad, font=font_inter, show="*",
                  bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                  insertbackground=dark_theme_colors["fg_entry"])
    e2.pack(pady=6)

    tk.Label(cad, text="Email:", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack()
    e3 = tk.Entry(cad, font=font_inter, show="*",
                  bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                  insertbackground=dark_theme_colors["fg_entry"])
    e3.pack(pady=6)

    tk.Label(cad, text="Dia de Nascimento:", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack()
    e4 = tk.Entry(cad, font=font_inter, show="*",
                  bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                  insertbackground=dark_theme_colors["fg_entry"])
    e4.pack(pady=6)

    tk.Label(cad, text="Mês de Nascimento:", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack()
    e5 = tk.Entry(cad, font=font_inter, show="*",
                  bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                  insertbackground=dark_theme_colors["fg_entry"])
    e5.pack(pady=6)

    tk.Label(cad, text="Ano de Nascimento:", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack()
    e6 = tk.Entry(cad, font=font_inter, show="*",
                  bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                  insertbackground=dark_theme_colors["fg_entry"])
    e6.pack(pady=6)

    tk.Label(cad, text="genero:", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack()
    e7 = tk.Entry(cad, font=font_inter, show="*",
                  bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["fg_entry"],
                  insertbackground=dark_theme_colors["fg_entry"])
    e7.pack(pady=6)

    

    def cadastrar():
        u = e1.get().strip()
        e = e2.get().strip()
        p = e3.get().strip()
        d = e4.get().strip()
        m = e5.get().strip()
        a = e6.get().strip()
        g = e7.get().strip()
        if not u or not g or not p or not d or not m or not a:
            messagebox.showwarning("Aviso", "Preencha tudo.")
            return
        try:
            signupController(root,e1, e2, e3, e4, e5, e6, e7)
            messagebox.showinfo("OK", "Cadastro criado!")
            cad.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # button de cadastrar com img
    if img_cadastrar_confirm:
        tk.Button(cad, image=img_cadastrar_confirm, command=cadastrar, bd=0, highlightthickness=0,
                  activebackground=dark_theme_colors["bg_main"]).pack(pady=20)
    else:
        tk.Button(cad, text="Cadastrar", width=20, height=2, command=cadastrar, font=font_inter,
                  bg=dark_theme_colors["purple_button"], fg=dark_theme_colors["fg_button"],
                  activebackground=dark_theme_colors["active_bg_button"], activeforeground=dark_theme_colors["fg_button"]).pack(pady=20)


#Tela de Login

def main():
    root = tk.Tk()
    
    
    global font_roboto, font_inter, font_roboto_big
    
    font_roboto = tkFont.Font(family="Roboto", size=14, weight="bold")
    font_roboto_big = tkFont.Font(family="Roboto", size=18, weight="bold")
    
    font_inter_light = tkFont.Font(family="Inter", size=10, weight="normal") 
    font_inter = tkFont.Font(family="Inter", size=12)

    root.title("Login")
    root.geometry("360x640")
    
    root.configure(bg=dark_theme_colors["bg_main"]) 
    
    
    img_entrar = carregar_icone("entrar_button.png")
    img_criar_cadastro = carregar_icone("criarcadastro_button.png")
    img_cadastrar_confirm = carregar_icone("cadastrar_button.png") 
    
    img_eye_open = carregar_icone("eye_open.png", tamanho=(20, 20)) 
    img_eye_closed = carregar_icone("eye_closed.png", tamanho=(20, 20))
    

    
    main_frame = tk.Frame(root, bg=dark_theme_colors["bg_main"])
    main_frame.pack(expand=True, fill="both")

    
    tk.Label(main_frame, text="Bem-vindo(a) de volta!", font=font_roboto_big, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack(pady=(50, 5))

    
    tk.Label(main_frame, text="É bom vê-lo(a) novamente! Por favor digite\nsuas informações.", 
             font=font_inter_light, justify="center",
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"]).pack(pady=(0, 30))

    
    tk.Label(main_frame, text="E-mail", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"], anchor="w").pack(fill="x", padx=40, pady=(10,0))
    
    entry_user_frame = tk.Frame(main_frame, bg=dark_theme_colors["bg_entry"], bd=1, relief="solid")
    entry_user_frame.pack(fill="x", padx=40)
    entry_user = tk.Entry(entry_user_frame, font=font_inter,
                          bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["placeholder_fg"],
                          insertbackground=dark_theme_colors["fg_entry"], 
                          bd=0, highlightthickness=0, relief="flat", width=25)
    entry_user.insert(0, "Seu e-mail")
    entry_user.bind("<FocusIn>", lambda event: on_entry_click(event, entry_user, "Seu e-mail"))
    entry_user.bind("<FocusOut>", lambda event: on_focus_out(event, entry_user, "Seu e-mail"))
    entry_user.pack(side="left", padx=10, pady=10, expand=True, fill="x")

    
    tk.Label(main_frame, text="Senha", font=font_inter, 
             bg=dark_theme_colors["bg_main"], fg=dark_theme_colors["fg_text"], anchor="w").pack(fill="x", padx=40, pady=(20,0))
    
    entry_pass_frame = tk.Frame(main_frame, bg=dark_theme_colors["bg_entry"], bd=1, relief="solid")
    entry_pass_frame.pack(fill="x", padx=40)
    entry_pass = tk.Entry(entry_pass_frame, show="*", font=font_inter,
                          bg=dark_theme_colors["bg_entry"], fg=dark_theme_colors["placeholder_fg"],
                          insertbackground=dark_theme_colors["fg_entry"], 
                          bd=0, highlightthickness=0, relief="flat", width=25)
    entry_pass.insert(0, "Sua senha")
    entry_pass.bind("<FocusIn>", lambda event: on_entry_click(event, entry_pass, "Sua senha"))
    entry_pass.bind("<FocusOut>", lambda event: on_focus_out(event, entry_pass, "Sua senha"))
    entry_pass.pack(side="left", padx=10, pady=10, expand=True, fill="x")

    
    def toggle_password_visibility():
        if entry_pass.cget("show") == "*":
            entry_pass.config(show="")
            eye_button.config(image=img_eye_open)
        else:
            entry_pass.config(show="*")
            eye_button.config(image=img_eye_closed)

    eye_button = tk.Button(entry_pass_frame, image=img_eye_closed, command=toggle_password_visibility,
                           bd=0, highlightthickness=0, bg=dark_theme_colors["bg_entry"],
                           activebackground=dark_theme_colors["bg_entry"])
    eye_button.pack(side="right", padx=(0,10))

    def fazer_login():
        # logica de login
        u = entry_user.get().strip()
        s = entry_pass.get().strip()

        # ignorar placeholders ao verificar login
        if u == "Seu e-mail": u = ""
        if s == "Sua senha": s = ""

        user = user_service.get_user(u)
        if not user:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return

        if user.password != s:
            messagebox.showerror("Erro", "Senha incorreta!")
            return

        messagebox.showinfo("OK", "Login bem-sucedido!")
        
        abrir_home(u, font_roboto, font_inter, font_roboto_big, root) 
        
        root.withdraw() 

    def abrir_cadastro():
        criar_cadastro(root, font_roboto, font_inter, img_cadastrar_confirm)


    # buttons de acao
    #-__________________________________________________________________________________________________________________
    if img_entrar:
        tk.Button(main_frame, image=img_entrar, command=lambda:loginController(root,entry_user,entry_pass), bd=0, highlightthickness=0,
                  activebackground=dark_theme_colors["bg_main"]).pack(pady=(40, 10), padx=40, fill="x")
    else:
        tk.Button(main_frame, text="Entrar", width=20, height=2, command=lambda:loginController(root,entry_user,entry_pass), font=font_inter,
                  bg=dark_theme_colors["purple_button"], fg=dark_theme_colors["fg_button"],
                  activebackground=dark_theme_colors["active_bg_button"], activeforeground=dark_theme_colors["fg_button"]).pack(pady=(40, 10), padx=40, fill="x")
    
    if img_criar_cadastro:
        tk.Button(main_frame, image=img_criar_cadastro, command=abrir_cadastro, bd=0, highlightthickness=0,
                  activebackground=dark_theme_colors["bg_main"]).pack (padx=40, fill="x")
    else:
        tk.Button(main_frame, text="Criar Cadastro", width=20, height=2, command=abrir_cadastro, font=font_inter,
                  bg=dark_theme_colors["purple_button"], fg=dark_theme_colors["fg_button"],
                  activebackground=dark_theme_colors["active_bg_button"], activeforeground=dark_theme_colors["fg_button"]).pack(padx=40, fill="x")


    # Refs
    
    root.image_refs = [img_entrar, img_criar_cadastro, img_cadastrar_confirm, img_eye_open, img_eye_closed] 
    
    root.mainloop()


