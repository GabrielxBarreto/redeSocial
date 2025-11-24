import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk 

# 1. Defis de Fallback e Importação Robusta 


# Cores e Fontes Fallback
SOLID_GRAY_BLOCK = "#3C3C3C" 
FALLBACK_COLORS = {
    "bg_main": "#1e1e1e",           # Fundo Principal Escuro
    "fg_text": "#ffffff",           # Texto Principal Branco
    "accent_color": "#6f42c1",      # Roxo (Cor de Destaque)
    "accent_color_hover": "#5a369a", # Roxo mais escuro para hover
    "bg_entry": SOLID_GRAY_BLOCK,   
    "bg_entry_border": SOLID_GRAY_BLOCK,
    "fg_secondary": "#aaaaaa",      # Cinza claro para texto auxiliar
    "bg_card": "#2e2e2e",           # Fundo dos cards (Posts/Projetos)
    "signup_link_fg": "#6f42c1"     
}
FALLBACK_FONT_TITLE = ("Roboto", 20, "bold")
FALLBACK_FONT_BIG = ("Roboto", 14, "bold")
FALLBACK_FONT_DEFAULT = ("Roboto", 12)
FALLBACK_WIDTH, FALLBACK_HEIGHT = 400, 600

# Tentativa de importação de utils_icons.py
try:
    from utils_icons import (
        colors,
        font_roboto_big,
        font_roboto,
        font_roboto_title,
        FRAME_WIDTH,
        FRAME_HEIGHT,
        setup_test_window,
    )
    # Garante que todas as cores necessárias estão presentes no dict 'colors'
    for key, value in FALLBACK_COLORS.items():
        if key not in colors:
             colors[key] = value

except ImportError:
    print("Aviso: Falha ao importar utils_icons.py. Usando cores e fontes padrão.")
    colors = FALLBACK_COLORS
    font_roboto_title = FALLBACK_FONT_TITLE
    font_roboto_big = FALLBACK_FONT_BIG
    font_roboto = FALLBACK_FONT_DEFAULT
    FRAME_WIDTH = FALLBACK_WIDTH
    FRAME_HEIGHT = FALLBACK_HEIGHT


# View Principal: ProjectsView

class ProjectsView(tk.Frame):
    """Tela para visualizar e adicionar projetos do GitHub."""
    
    def __init__(self, master, switch_view_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.switch_view_callback = switch_view_callback
        
        self.config(bg=colors["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.pack_propagate(False)
        
        # Simulação de dados de projetos
        self.projects_data = [
            {"title": "MIAU App Tkinter", "user": "alan lindo", "link": "github.com/miau/app", "desc": "Projeto da rede social, focado em Tkinter e Pygame."},
            {"title": "Algoritmos de IA", "user": "Outro Dev", "link": "github.com/dev/ia", "desc": "Implementação de redes neurais simples em Python."},
        ]

        self._create_widgets()

    def _create_widgets(self):
        # Frame do Cabeçalho
        header_frame = tk.Frame(self, bg=colors["bg_main"], padx=10, pady=15)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame,
                 text="Projects ",
                 font=font_roboto_title,
                 fg=colors["accent_color"],
                 bg=colors["bg_main"]).pack(side="left")
        
        # Botão para Adicionar Novo Projeto 
        add_button = tk.Button(header_frame,
                               
                               command=self._show_add_project_placeholder,
                               text="New Project",
                               bg=colors["accent_color"],
                               fg=colors["fg_text"],
                               font=font_roboto,
                               bd=0,
                               padx=10,
                               pady=5,
                               activebackground=colors["accent_color_hover"],
                               activeforeground=colors["fg_text"],
                               cursor="hand2")
        add_button.pack(side="right")

        
        self._create_scrollable_list()
        
        
        self._load_projects()

    def _create_scrollable_list(self):
        
        self.canvas = tk.Canvas(self, bg=colors["bg_main"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, bg=colors["bg_main"])
        
        
        self.projects_container = tk.Frame(self.canvas, bg=colors["bg_main"])
        
        # Config do Canvas
        self.projects_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.projects_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Permite rolar o Canvas usando o scroll do mouse."""
        # Se for no Windows/Linux, é event.delta. No Mac, pode ser diferente, mas essa é a solução padrão.
        if event.num == 5 or event.delta == -120:  
            self.canvas.yview_scroll(1, "unit")
        elif event.num == 4 or event.delta == 120:  
            self.canvas.yview_scroll(-1, "unit")
        
    def _load_projects(self):
        # Limpa projetos existentes
        for widget in self.projects_container.winfo_children():
            widget.destroy()
            
        if not self.projects_data:
            tk.Label(self.projects_container,
                     text="Nenhum projeto encontrado. Adicione o primeiro!",
                     bg=colors["bg_main"],
                     fg=colors["fg_secondary"],
                     font=font_roboto).pack(pady=50)
            return

        for project in self.projects_data:
            self._create_project_card(project)
            
    def _create_project_card(self, project):
        """Cria um card visual para um projeto."""
        
        card = tk.Frame(self.projects_container, 
                        bg=colors["bg_card"], 
                        padx=15, 
                        pady=15, 
                        bd=0,
                        relief="flat")
        card.pack(fill="x", padx=10, pady=8)
        
        # Título e Usuário
        title_frame = tk.Frame(card, bg=colors["bg_card"])
        title_frame.pack(fill="x", pady=(0, 5))
        
        tk.Label(title_frame,
                 text=project["title"],
                 font=font_roboto_big,
                 fg=colors["accent_color"],
                 bg=colors["bg_card"],
                 anchor="w").pack(side="left")
        
        tk.Label(title_frame,
                 text=f'por {project["user"]}',
                 font=font_roboto,
                 fg=colors["fg_secondary"],
                 bg=colors["bg_card"],
                 anchor="e").pack(side="right")
                 
        # Descrição
        tk.Label(card,
                 text=project["desc"],
                 font=font_roboto,
                 fg=colors["fg_text"],
                 bg=colors["bg_card"],
                 wraplength=FRAME_WIDTH - 50,
                 justify="left",
                 anchor="w").pack(fill="x", pady=5)
                 
        # Link do GitHub
        link_label = tk.Label(card,
                              text=f'Link: {project["link"]}',
                              font=font_roboto,
                              fg=colors["signup_link_fg"], 
                              bg=colors["bg_card"],
                              cursor="hand2",
                              anchor="w")
        link_label.pack(fill="x", pady=(5, 0))
       
        link_label.bind("<Button-1>", lambda e: messagebox.showinfo("Abrir Link", f"Simulação: Abrir link no navegador:\n{project['link']}"))


    def _show_add_project_placeholder(self):
        """Exibe uma mensagem placeholder para a funcionalidade de adicionar projeto."""
        messagebox.showinfo("New Project", "Implementação da função de adicionar projeto.")
        
 

#  Teste de Execução Individual 

if __name__ == "__main__":
    
    # Config do ambiente de teste 
    root = tk.Tk()
    root.title("Projects View Teste")
    root.geometry(f"{FALLBACK_WIDTH}x{FALLBACK_HEIGHT}")
    
    test_frame = tk.Frame(root)
    test_frame.pack(fill="both", expand=True)
    
    def switch_view_mock(view_name):
        messagebox.showinfo("Navegação", f"Navegar para a View: {view_name}")
    
    projects_app = ProjectsView(
        test_frame,
        switch_view_mock
    )
    projects_app.pack(fill="both", expand=True)
    
    root.mainloop()