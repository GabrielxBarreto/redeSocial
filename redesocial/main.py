
import tkinter as tk
import tkinter.font as tkFont

# Importa Configurações e Utilitários
from .config.settings import (
    DARK_THEME_COLORS, carregar_icone, inicializar_fontes,
    on_entry_click, on_focus_out,
    font_roboto, font_inter, font_roboto_big 
)

# Importa Views e Controllers
from .views.signup_view import criar_cadastro
from .controller.authController import loginController


def main():
    root = tk.Tk()
    colors = DARK_THEME_COLORS
    
    # Inicializa as fontes (as variáveis em settings.py são preenchidas)
    inicializar_fontes() 
    
    # Fonte local para a descrição da tela de login
    font_inter_light = tkFont.Font(family="Inter", size=10, weight="normal") 

    root.title("Login")
    root.geometry("360x640")
    
    # Configura a cor DEPOIS da criação (CORREÇÃO DO TypeError)
    root.configure(bg=colors["bg_main"]) 
    
    # --- Carregamento de Ícones ---
    img_entrar = carregar_icone("entrar_button.png")
    img_criar_cadastro = carregar_icone("criarcadastro_button.png")
    img_cadastrar_confirm = carregar_icone("cadastrar_button.png") 
    img_eye_open = carregar_icone("eye_open.png", tamanho=(20, 20)) 
    img_eye_closed = carregar_icone("eye_closed.png", tamanho=(20, 20))
    
    # --- Layout da Tela de Login ---
    main_frame = tk.Frame(root, bg=colors["bg_main"]); main_frame.pack(expand=True, fill="both")

    tk.Label(main_frame, text="Bem-vindo(a) de volta!", font=font_roboto_big, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(50, 5))
    tk.Label(main_frame, text="É bom vê-lo(a) novamente! Por favor digite\nsuas informações.", font=font_inter_light, justify="center", bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(0, 30))

    # E-MAIL
    tk.Label(main_frame, text="E-mail", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"], anchor="w").pack(fill="x", padx=40, pady=(10,0))
    entry_user_frame = tk.Frame(main_frame, bg=colors["bg_entry"], bd=1, relief="solid"); entry_user_frame.pack(fill="x", padx=40)
    entry_user = tk.Entry(entry_user_frame, font=font_inter, bg=colors["bg_entry"], fg=colors["placeholder_fg"], insertbackground=colors["fg_entry"], bd=0, highlightthickness=0, relief="flat", width=25)
    entry_user.insert(0, "Seu e-mail"); entry_user.bind("<FocusIn>", lambda event: on_entry_click(event, entry_user, "Seu e-mail")); entry_user.bind("<FocusOut>", lambda event: on_focus_out(event, entry_user, "Seu e-mail")); entry_user.pack(side="left", padx=10, pady=10, expand=True, fill="x")

    # SENHA
    tk.Label(main_frame, text="Senha", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"], anchor="w").pack(fill="x", padx=40, pady=(20,0))
    entry_pass_frame = tk.Frame(main_frame, bg=colors["bg_entry"], bd=1, relief="solid"); entry_pass_frame.pack(fill="x", padx=40)
    entry_pass = tk.Entry(entry_pass_frame, show="*", font=font_inter, bg=colors["bg_entry"], fg=colors["placeholder_fg"], insertbackground=colors["fg_entry"], bd=0, highlightthickness=0, relief="flat", width=25)
    entry_pass.insert(0, "Sua senha"); entry_pass.bind("<FocusIn>", lambda event: on_entry_click(event, entry_pass, "Sua senha")); entry_pass.bind("<FocusOut>", lambda event: on_focus_out(event, entry_pass, "Sua senha")); entry_pass.pack(side="left", padx=10, pady=10, expand=True, fill="x")

    # Toggle Password Visibility
    def toggle_password_visibility():
        if entry_pass.cget("show") == "*":
            entry_pass.config(show="")
            eye_button.config(image=img_eye_open)
        else:
            entry_pass.config(show="*")
            eye_button.config(image=img_eye_closed)

    eye_button = tk.Button(entry_pass_frame, image=img_eye_closed, command=toggle_password_visibility, bd=0, highlightthickness=0, bg=colors["bg_entry"], activebackground=colors["bg_entry"]); eye_button.pack(side="right", padx=(0,10))

    # Funções de Ação (Chamando as views modulares)
    def abrir_cadastro():
        criar_cadastro(root, img_cadastrar_confirm)

    # Botões (Entrar chama o Controller)
    if img_entrar:
        tk.Button(main_frame, image=img_entrar, command=lambda:loginController(root,entry_user,entry_pass), bd=0, highlightthickness=0, activebackground=colors["bg_main"]).pack(pady=(40, 10), padx=40, fill="x")
    else:
        tk.Button(main_frame, text="Entrar", width=20, height=2, command=lambda:loginController(root,entry_user,entry_pass), font=font_inter, bg=colors["purple_button"], fg=colors["fg_button"], activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"]).pack(pady=(40, 10), padx=40, fill="x")
    
    if img_criar_cadastro:
        tk.Button(main_frame, image=img_criar_cadastro, command=abrir_cadastro, bd=0, highlightthickness=0, activebackground=colors["bg_main"]).pack (padx=40, fill="x")
    else:
        tk.Button(main_frame, text="Criar Cadastro", width=20, height=2, command=abrir_cadastro, font=font_inter, bg=colors["purple_button"], fg=colors["fg_button"], activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"]).pack(padx=40, fill="x")

    root.image_refs = [img_entrar, img_criar_cadastro, img_cadastrar_confirm, img_eye_open, img_eye_closed] 
    
    root.mainloop()


if __name__ == "__main__":
    main()