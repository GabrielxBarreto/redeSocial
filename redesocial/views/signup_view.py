# redesocial/views/signup_view.py

import tkinter as tk
from tkinter import messagebox

from ..config.settings import DARK_THEME_COLORS, font_roboto, font_inter
from ..controller.authController import signupController 


def criar_cadastro(root, img_cadastrar_confirm):
    """Cria e exibe a tela de Cadastro."""
    colors = DARK_THEME_COLORS
    
    cad = tk.Toplevel(root, bg=colors["bg_main"]) 
    cad.title("Cadastro")
    # Aumentando o tamanho para caber todos os campos
    cad.geometry("360x600") 

    # Frame para centralizar o conteúdo e permitir rolagem se necessário (simplificado aqui)
    content_frame = tk.Frame(cad, bg=colors["bg_main"])
    content_frame.pack(padx=20, pady=20)

    # --- Widgets de Entrada (Mantidos) ---
    tk.Label(content_frame, text="Criar Conta", font=font_roboto, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(0, 10))

    tk.Label(content_frame, text="Usuário:", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(5,0), anchor="w")
    e1 = tk.Entry(content_frame, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"]); e1.pack(pady=(0, 5))

    tk.Label(content_frame, text="Senha:", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(5,0), anchor="w")
    e2 = tk.Entry(content_frame, font=font_inter, show="*", bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"]); e2.pack(pady=(0, 5))

    tk.Label(content_frame, text="Email:", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(5,0), anchor="w")
    e3 = tk.Entry(content_frame, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"]); e3.pack(pady=(0, 5))

    tk.Label(content_frame, text="Dia de Nascimento:", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(5,0), anchor="w")
    e4 = tk.Entry(content_frame, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"]); e4.pack(pady=(0, 5))

    tk.Label(content_frame, text="Mês de Nascimento:", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(5,0), anchor="w")
    e5 = tk.Entry(content_frame, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"]); e5.pack(pady=(0, 5))

    tk.Label(content_frame, text="Ano de Nascimento:", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(5,0), anchor="w")
    e6 = tk.Entry(content_frame, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"]); e6.pack(pady=(0, 5))

    tk.Label(content_frame, text="Gênero:", font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(pady=(5,0), anchor="w")
    e7 = tk.Entry(content_frame, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"]); e7.pack(pady=(0, 5))

    def cadastrar():
        # Chama o controller com todos os campos de entrada (widgets)
        signupController(root, e1, e3, e2, e4, e5, e6, e7) # Ordem: user, email, pass, day, month, year, gender
        # Se o login for bem-sucedido dentro do controller, a janela `cad` deve ser destruída.
        # Caso contrário, ela permanece aberta para correção.
        
        # NOTE: Se loginController for bem-sucedido, ele faz root.withdraw().
        # Precisamos garantir que `cad` (o Toplevel) feche:
        if root.winfo_ismapped() == 0: # Se a janela principal foi escondida, o login foi OK
             cad.destroy()

    # Botão de Cadastrar
    if img_cadastrar_confirm:
        tk.Button(content_frame, image=img_cadastrar_confirm, command=cadastrar, bd=0, highlightthickness=0,
                  activebackground=colors["bg_main"]).pack(pady=(20, 10))
    else:
        tk.Button(content_frame, text="Cadastrar", width=20, height=2, command=cadastrar, font=font_inter,
                  bg=colors["purple_button"], fg=colors["fg_button"],
                  activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"]).pack(pady=(20, 10))
    
    cad.image_ref = img_cadastrar_confirm # Mantém referência da imagem