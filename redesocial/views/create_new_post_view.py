import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk 
import tkinter.font as tkFont 
from .config_layout import *
from ..service.userService import new_post

from ..config.settings import (
    DARK_THEME_COLORS, carregar_icone, font_roboto, 
    font_inter, font_roboto_big, on_entry_click, on_focus_out
)


 # --- Conteúdo da Aba NOVO POST ---
f = frames["Novo Post"]
tk.Label(f, text="Criar Novo Post", font=font_roboto_big, bg=colors["bg_frame"], fg=colors["fg_text"]).pack(pady=10)
tk.Button(f, text="Publicar", command=new_post, width=20, height=2, font=font_inter, bg=colors["bg_button"], fg=colors["fg_button"], activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"]).pack(pady=10)
