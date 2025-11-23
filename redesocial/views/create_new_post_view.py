import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk 
import tkinter.font as tkFont 
from .config_layout import *
from ..config.settings import (
    DARK_THEME_COLORS, carregar_icone, font_roboto, 
    font_inter, font_roboto_big, on_entry_click, on_focus_out
)

colors = DARK_THEME_COLORS 
container = tk.Frame(home, bg=colors["bg_main"]); container.pack(expand=True, fill="both")
frames = {}; abas_principais = ["Home", "Novo Post", "Projetos", "Ranking", "Perfil"]
for aba in abas_principais:
    frames[aba] = tk.Frame(container, bg=colors["bg_frame"]) 

 # --- Conteúdo da Aba NOVO POST ---
f = frames["Novo Post"]
tk.Label(f, text="Criar Novo Post", font=font_roboto_big, bg=colors["bg_frame"], fg=colors["fg_text"]).pack(pady=10)
post_box = scrolledtext.ScrolledText(f, width=42, height=10, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"], wrap="word"); post_box.pack(padx=10, pady=5)
tk.Button(f, text="Publicar", command=publicar, width=20, height=2, font=font_inter, bg=colors["bg_button"], fg=colors["fg_button"], activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"]).pack(pady=10)
