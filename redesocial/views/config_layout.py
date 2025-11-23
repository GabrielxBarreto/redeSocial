
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk 
import tkinter.font as tkFont 
from ..config.settings import (
    DARK_THEME_COLORS, carregar_icone, font_roboto, 
    font_inter, font_roboto_big, on_entry_click, on_focus_out
)

#--- Configuração Inicial da Janela ---
home = tk.Toplevel(bg=DARK_THEME_COLORS["bg_main"]) 
home.title("Home")
home.geometry("420x720")
home.resizable(False, False) 
colors = DARK_THEME_COLORS 
tamanho_icone = (30, 30) 

# Adicionando ícones (Mantenha as imagens na pasta img/)
icones = {
    "Home": carregar_icone("home_image.png", tamanho=tamanho_icone),
    "Novo Post": carregar_icone("newpost_image.png", tamanho=tamanho_icone),
    "Projetos": carregar_icone("projeto_image.png", tamanho=tamanho_icone), 
    "Ranking": carregar_icone("ranking_image.png", tamanho=tamanho_icone),
    "Perfil": carregar_icone("user_image.png", tamanho=tamanho_icone),
    "cover_image": carregar_icone("cover_image.png", tamanho=(420, 150)), 
    "profile_pic": carregar_icone("profile_pic.png", tamanho=(80, 80)),   
    "back_arrow": carregar_icone("back_arrow.png", tamanho=(24, 24)),     
    "friends_icon": carregar_icone("friends_icon.png", tamanho=(20, 20)), 
    "location_icon": carregar_icone("location_icon.png", tamanho=(16,16)), 
    "education_icon": carregar_icone("education_icon.png", tamanho=(16,16)), 
    "post_image": carregar_icone("post_image.png", tamanho=(380, 200)) 
}
botoes_barra = []

 # --- Conteúdo Central ---
container = tk.Frame(home, bg=colors["bg_main"]); container.pack(expand=True, fill="both")
post_box = scrolledtext.ScrolledText(None, width=42, height=10, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"], wrap="word"); post_box.pack(padx=10, pady=5)

frames = {}; abas_principais = ["Home", "Novo Post", "Projetos", "Ranking", "Perfil"]
for aba in abas_principais:
    frames[aba] = tk.Frame(container, bg=colors["bg_frame"]) 
