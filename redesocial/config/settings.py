
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk 
import os
import json
import sys
from redesocial.service.authService import AuthService
# --- variaveis Globais de fontes ---
font_roboto = None
font_inter = None
font_roboto_big = None 

def inicializar_fontes():
    """inicializa as fontes e as define como globais"""
    global font_roboto, font_inter, font_roboto_big
    if font_roboto is None:
        font_roboto = tkFont.Font(family="Roboto", size=14, weight="bold")
        font_roboto_big = tkFont.Font(family="Roboto", size=18, weight="bold")
        font_inter = tkFont.Font(family="Inter", size=12)

# --- Cores do Tema ---
DARK_THEME_COLORS = {
    "bg_main": "#F0F0F0", "fg_text": "#1E1E1E", "bg_frame": "#E8E8E8", "bg_button": "#505050",     
    "fg_button": "#FFFFFF", "bg_entry": "#FFFFFF", "fg_entry": "#1E1E1E", "border": "#CCCCCC",         
    "active_bg_button": "#6A6A6A", "placeholder_fg": "#A0A0A0", "purple_button": "#4B0082", 
    "bottom_bar_bg": "#1E1E1E", "icon_inactive_fg": "#8A2BE2", "icon_active_fg": "#E6E6FA", 
    "button_bar_bg": "#1E1E1E"   
}

# --- caminhos e service ---

# BASE_DIR é a pasta 'redesocial/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
# PROJECT_ROOT é o nível acima de 'redesocial/'
PROJECT_ROOT = os.path.dirname(BASE_DIR) 
USERS_JSON = os.path.join(PROJECT_ROOT, "usuarios.json")
IMG_DIR = os.path.join(BASE_DIR, "views", "img")

# tenta importar AuthService, senão usa SimpleUserService

auth_service = AuthService()
 
# variável de serviço que sera importada pelos controllers
USER_AUTH_SERVICE = auth_service


# --- funcoes de utilitario ---

def carregar_icone(nome_arquivo, tamanho=None):
    """carrega o icone do diretório views"""
    path = os.path.join(IMG_DIR, nome_arquivo) 
    try:
        img_pil = Image.open(path)
        if nome_arquivo.endswith(".png") and tamanho: 
            img_pil = img_pil.resize(tamanho) 
        return ImageTk.PhotoImage(img_pil)
    except FileNotFoundError:
        return None
    except Exception:
        return None


def on_entry_click(event, entry_widget, placeholder_text):
    """logica do placeholder para campo de entrada"""
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")
        entry_widget.config(fg=DARK_THEME_COLORS["fg_entry"], show="" if entry_widget.cget("show") != "*" else entry_widget.cget("show"))

def on_focus_out(event, entry_widget, placeholder_text):
    """logica do placeholder"""
    if entry_widget.get() == "":
        entry_widget.insert(0, placeholder_text)
        entry_widget.config(fg=DARK_THEME_COLORS["placeholder_fg"], show="")