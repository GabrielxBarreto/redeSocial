import tkinter as tk
from tkinter import messagebox
import os 
import sys
from PIL import Image, ImageTk 



# 1. Defis de Fallback e Importação Robusta (Replicando as definições de cor)


# Defs de cor para manter a consistência visual
SOLID_GRAY_BLOCK = "#3C3C3C" 
FALLBACK_COLORS = {
    "bg_main": "#1e1e1e",           # Fundo Principal Escuro
    "fg_text": "#ffffff",           # Texto Principal Branco
    "accent_color": "#6f42c1",      # Roxo (Cor de Destaque)
    "accent_color_hover": "#5a369a", # Roxo mais escuro para hover
    "bg_entry": SOLID_GRAY_BLOCK,   
    "bg_entry_border": SOLID_GRAY_BLOCK,
    "fg_secondary": "#aaaaaa",      # Cinza claro para texto auxiliar
    "icon_active_fg": SOLID_GRAY_BLOCK,
    "signup_link_fg": "#6f42c1",    
    "signup_link_active_fg": "#5a369a", 
}
FALLBACK_FONT_BIG = ("Roboto", 18, "bold")
FALLBACK_FONT_DEFAULT = ("Roboto", 12)
FALLBACK_FONT_SMALL = ("Inter", 10)
FALLBACK_WIDTH, FALLBACK_HEIGHT = 400, 600


# import do utils_icons, definindo fallbacks se a importação falhar
try:
    from utils_icons import (
        colors,
        font_roboto_big,
        font_roboto,
        FRAME_WIDTH,
        FRAME_HEIGHT,
        setup_test_window,
        font_inter_small
    )
    
    for key, value in FALLBACK_COLORS.items():
        if key not in colors:
             colors[key] = value

except ImportError:
    print("Aviso: Falha ao importar utils_icons.py. Usando cores e fontes padrão.")
    colors = FALLBACK_COLORS
    font_roboto_big = FALLBACK_FONT_BIG
    font_roboto = FALLBACK_FONT_DEFAULT
    font_inter_small = FALLBACK_FONT_SMALL
    FRAME_WIDTH = FALLBACK_WIDTH
    FRAME_HEIGHT = FALLBACK_HEIGHT
    setup_test_window = None


# View Principal: WelcomeView

class WelcomeView(tk.Frame):
    """Tela de boas-vindas inicial com o logo e botão para começar o cadastro."""
    
    
    logo_image_tk = None
    
    def __init__(self, master, switch_view_callback=None):
        super().__init__(master)
        self.switch_view_callback = switch_view_callback
        
        self.config(bg=colors["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.pack_propagate(False)

        self._create_widgets()
        
    def _load_image(self, relative_path):
        """Carrega a imagem de forma robusta usando o caminho absoluto do script.
           Aumentado o target_size para (180, 180)."""
        try:
            # Obtém o diretório do script atual 
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            #Constroi o caminho completo para a imagem
            full_path = os.path.join(script_dir, relative_path)

            # Tenta carregar a imagem do caminho completo
            original_image = Image.open(full_path)
            
            # Novo tamanho para o redimensionamento
            target_size = (180, 180) 
            resized_image = original_image.resize(target_size, Image.Resampling.LANCZOS)
            
            # Converte para PhotoImage para uso no Tkinter
            self.logo_image_tk = ImageTk.PhotoImage(resized_image)
            return self.logo_image_tk
            
        except FileNotFoundError:
            # debug
            print(f"ERRO: Arquivo de imagem não encontrado no caminho: {full_path}")
            return None
        except Exception as e:
            print(f"ERRO ao carregar ou processar a imagem: {e}")
            return None

        
    def _create_widgets(self):
        
        content_frame = tk.Frame(self, bg=colors["bg_main"])
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        
        # Logo 
        logo_path = os.path.join("img", "logomiau.png")
        self.logo_image_tk = self._load_image(logo_path)
        
        if self.logo_image_tk:
          
            logo_label = tk.Label(content_frame, 
                                  image=self.logo_image_tk, 
                                  bg=colors["bg_main"])
            logo_label.pack(pady=(20, 10))
        else:
            # Fallback 
            tk.Label(content_frame,
                     text="[LOGO MIAU - FALHA AO CARREGAR]",
                     font=("Roboto", 12),
                     bg=colors["bg_main"],
                     fg="red").pack(pady=(20, 10))


        
        tk.Label(content_frame,
                 text="MIAU",
                 font=("Roboto", 32, "bold"),
                 bg=colors["bg_main"],
                 fg=colors["accent_color"]).pack(pady=(10, 5))
        
        
        tk.Label(content_frame,
                 text="Seja Bem-Vindo ao\nMinha Interação Acadêmica Universitária!",
                 font=font_roboto,
                 bg=colors["bg_main"],
                 fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]),
                 justify=tk.CENTER).pack(pady=(5, 50))
        
        # 4. Botão Começar
        start_button = tk.Button(content_frame,
                                 text="Começar",
                                 command=lambda: self._go_to_view("signin"),
                                 bg=colors["accent_color"],
                                 fg=colors["fg_text"],
                                 font=font_roboto_big,
                                 width=20,
                                 height=2,
                                 bd=0,
                                 activebackground=colors.get("accent_color_hover", FALLBACK_COLORS["accent_color_hover"]),
                                 activeforeground=colors["fg_text"],
                                 cursor="hand2")
        start_button.pack(pady=(0, 20))
        
    def _go_to_view(self, view_name):
        """Chama o callback para trocar de view."""
        if self.switch_view_callback:
            self.switch_view_callback(view_name)
        else:
            messagebox.showinfo("Navegação Mock", f"Ação de ir para a View: {view_name}")


# Teste de Execução Individual

