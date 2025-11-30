import tkinter as tk
from tkinter import messagebox
from ..service.userService import publish_project
import os
from PIL import Image, ImageTk 
from ..data.projectsData import projects_df
import pandas as pd
import webbrowser
# 1. Defis de Fallback e Importação Robusta 

# Cores e Fontes Fallback
SOLID_GRAY_BLOCK = "#3C3C3C" 
FALLBACK_COLORS = {
    "bg_main": "#1e1e1e",           # Fundo Principal Escuro
    "fg_text": "#ffffff",            # Texto Principal Branco
    "accent_color": "#6f42c1",      # Roxo (Cor de Destaque)
    "accent_color_hover": "#5a369a", # Roxo mais escuro para hover
    "bg_entry": SOLID_GRAY_BLOCK,   
    "bg_entry_border": SOLID_GRAY_BLOCK,
    "fg_secondary": "#aaaaaa",      # Cinza claro para texto auxiliar
    "bg_card": "#2e2e2e",            # Fundo dos cards (Posts/Projetos)
    "signup_link_fg": "#6f42c1",
    "icon_inactive_fg": "#999999", 
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


# ------------------------------
#   VIEW PRINCIPAL: ProjectsView
# ------------------------------

class ProjectsView(tk.Frame):

    def __init__(self, master, session, switch_view_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.switch_view_callback = switch_view_callback
        self.session = session
        
        self.config(bg=colors["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.pack_propagate(False)
        
        self.projects_data = [
            {"title": "MIAU App Tkinter", "user": "alan lindo", "link": "github.com/miau/app", "desc": "Projeto da rede social, focado em Tkinter e Pygame."},
            {"title": "Algoritmos de IA", "user": "Outro Dev", "link": "github.com/dev/ia", "desc": "Implementação de redes neurais simples em Python."},
        ]

        self._create_widgets()

    def _create_widgets(self):

        header_frame = tk.Frame(self, bg=colors["bg_main"], padx=10, pady=15)
        header_frame.pack(fill="x")

        header_frame.columnconfigure(0, weight=0)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=0)

        # Botão Voltar
        def go_back():
            if self.switch_view_callback:
                self.switch_view_callback("home")

        back_button = tk.Button(
            header_frame,
            text="< Voltar",
            command=go_back,
            font=font_roboto,
            bg=colors["bg_main"],
            fg=colors["icon_inactive_fg"],
            bd=0,
            activebackground=colors["bg_main"],
            activeforeground=colors["accent_color"],
            cursor="hand2"
        )
        back_button.grid(row=0, column=0, sticky='w', padx=(0, 15))

        tk.Label(
            header_frame,
            text="Projects",
            font=font_roboto_title,
            fg=colors["accent_color"],
            bg=colors["bg_main"]
        ).grid(row=0, column=1, sticky='we')

        # Botão Novo
        add_button = tk.Button(
            header_frame,
            command=self._open_new_project_modal,
            text="+ Novo",
            bg=colors["accent_color"],
            fg=colors["fg_text"],
            font=font_roboto,
            bd=0,
            padx=10,
            pady=5,
            activebackground=colors["accent_color_hover"],
            activeforeground=colors["fg_text"],
            cursor="hand2"
        )
        add_button.grid(row=0, column=2, sticky='e')

        
        self._create_scrollable_list()
        self._load_projects()

    # ------------------------------
    #   LISTAGEM COM SCROLL
    # ------------------------------

    def _create_scrollable_list(self):

        self.canvas = tk.Canvas(self, bg=colors["bg_main"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.projects_container = tk.Frame(self.canvas, bg=colors["bg_main"])

        self.projects_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.window_item = self.canvas.create_window((0, 0), window=self.projects_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "unit")

    def _load_projects(self):

        for widget in self.projects_container.winfo_children():
            widget.destroy()

        if projects_df.empty:
            tk.Label(
                self.projects_container,
                text="Nenhum projeto encontrado. Adicione o primeiro!",
                bg=colors["bg_main"],
                fg=colors["fg_secondary"],
                font=font_roboto
            ).pack(pady=50)
            return
        
        filtered = projects_df[projects_df["author_id"] == self.session]
        for _, project in filtered.iterrows():
            self._create_project_card(project)

    # -------------
    #  EXPANSÃO
    # -------------

    def _toggle_details(self, frame, label, btn):
        if label.winfo_ismapped():
            label.pack_forget()
            btn.config(text="Ver mais")
        else:
            label.pack(fill="x", pady=(10, 0))
            btn.config(text="Ocultar")

    # ------------------------------
    #  CARD DE PROJETO + BOTÃO
    # ------------------------------

    def _create_project_card(self, project):

        card = tk.Frame(
            self.projects_container,
            bg=colors["bg_card"],
            padx=15,
            pady=15,
            bd=0
        )
        card.pack(fill="x", padx=10, pady=8)

        title_frame = tk.Frame(card, bg=colors["bg_card"])
        title_frame.pack(fill="x", pady=(0, 5))

        tk.Label(
            title_frame,
            text=project["title"],
            font=font_roboto_big,
            fg=colors["accent_color"],
            bg=colors["bg_card"],
            anchor="w"
        ).pack(side="left")

        tk.Label(
            title_frame,
            text=f'por {project["author"]}',
            font=font_roboto,
            fg=colors["fg_secondary"],
            bg=colors["bg_card"],
            anchor="e"
        ).pack(side="right")

        # Descrição principal
        tk.Label(
            card,
            text=project["description"],
            font=font_roboto,
            fg=colors["fg_text"],
            bg=colors["bg_card"],
            wraplength=FRAME_WIDTH - 50,
            justify="left",
            anchor="w"
        ).pack(fill="x", pady=5)

        # Link
        link_label = tk.Label(
            card,
            text=f'Link: {project["link_github"]}',
            font=font_roboto,
            fg=colors["signup_link_fg"],
            bg=colors["bg_card"],
            cursor="hand2",
            anchor="w"
        )
        link_label.pack(fill="x", pady=(5, 0))
        
        link_label.bind(
            "<Button-1>",
            lambda e: webbrowser.open(project['link_github'])
        )

        # ---------------------
        #  NOVO BOTÃO EXPANDIR
        # ---------------------

        details_label = tk.Label(
            card,
            text=f"✨ SCORE DO PROJETO: {project['score']}\n\n📝 Autor ID: {project['author_id']}",
            font=font_roboto,
            fg=colors["fg_secondary"],
            bg=colors["bg_card"],
            justify="left",
            anchor="w",
            wraplength=FRAME_WIDTH - 50
        )

        toggle_btn = tk.Button(
            card,
            text="Ver mais",
            font=font_roboto,
            bg=colors["bg_entry"],
            fg=colors["fg_text"],
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=lambda: self._toggle_details(card, details_label, toggle_btn)
        )
        toggle_btn.pack(pady=(10, 0))

    # ----------------------------------------------------
    #   MODAL FLUTUANTE (NOVO PROJETO)
    # ----------------------------------------------------
    def _open_new_project_modal(self):

        overlay = tk.Frame(self.master, bg="black")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay.bind("<Button-1>", lambda e: overlay.destroy())

        modal = tk.Frame(
            overlay,
            bg=colors["bg_card"],
            padx=20,
            pady=20
        )
        modal.place(relx=0.5, rely=0.5, anchor="center")

        modal.bind("<Button-1>", lambda e: "break")

        tk.Label(
            modal,
            text="Novo Projeto",
            font=font_roboto_title,
            fg=colors["accent_color"],
            bg=colors["bg_card"]
        ).pack(pady=(0, 20))

        def create_input(label):
            tk.Label(
                modal,
                text=label,
                bg=colors["bg_card"],
                fg=colors["fg_text"],
                font=font_roboto
            ).pack(anchor="w")

            entry = tk.Entry(
                modal,
                font=font_roboto,
                bg=colors["bg_entry"],
                fg=colors["fg_text"],
                insertbackground=colors["fg_text"],
                bd=0
            )
            entry.pack(fill="x", pady=(0, 10))

            return entry

        title_entry = create_input("Título do Projeto:")
        user_entry = create_input("Autor:")
        link_entry = create_input("Link do GitHub:")
        desc_entry = create_input("Descrição:")
       
        btn_frame = tk.Frame(modal, bg=colors["bg_card"])
        btn_frame.pack(fill="x", pady=(15, 0))

        tk.Button(
            btn_frame,
            text="Cancelar",
            command=lambda: overlay.destroy(),
            bg=colors["bg_entry"],
            fg=colors["fg_text"],
            font=font_roboto,
            padx=10,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side="left", padx=5)

        def publish_load():
            publish_project(self.session, user_entry, title_entry, link_entry, desc_entry)
            messagebox.showinfo(
                "Projeto Criado",
                "Modal funcionando perfeitamente.\n(Apenas UI)"
            )
            overlay.destroy()
        
        tk.Button(
            btn_frame,
            text="Publicar",
            command=publish_load,
            bg=colors["accent_color"],
            fg=colors["fg_text"],
            font=font_roboto,
            padx=15,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side="right", padx=5)
    
# ----------------------------------------------------
#   TESTE
# ----------------------------------------------------
if __name__ == "__main__":

    root = tk.Tk()
    root.title("Projects View Teste")
    root.geometry(f"{FALLBACK_WIDTH}x{FALLBACK_HEIGHT}")

    test_frame = tk.Frame(root)
    test_frame.pack(fill="both", expand=True)
    
    def switch_view_mock(v):
        messagebox.showinfo("Navegar", f"View: {v}")

    ProjectsView(test_frame, switch_view_mock).pack(fill="both", expand=True)

    root.mainloop()
