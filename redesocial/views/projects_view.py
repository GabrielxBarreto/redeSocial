import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import Image, ImageTk

# Importações necessárias do arquivo de utilidades (utils_icons.py).
from utils_icons import (
    colors, font_roboto_big, font_inter, 
    MOCK_PROJECTS_DATA, setup_test_window, ICON_SIZE_NAV
)

# Constantes de layout
PROJECT_FRAME_BG = colors["bg_frame"]
PROJECT_BORDER_COLOR = colors["bg_main"]

def criar_card_projeto(container, project_data):
    """
    Cria um card de projeto individual com informações detalhadas, incluindo
    título, proprietário, descrição, status, colaboradores, tecnologia e progresso.
    
    Args:
        container (tk.Widget): O widget pai onde o projeto será colocado.
        project_data (dict): Dicionário contendo dados do projeto.
        
    Returns:
        tk.Frame: O frame do card do projeto.
    """
    card = tk.Frame(container, bg=PROJECT_FRAME_BG, padx=15, pady=15, 
                    highlightbackground=PROJECT_BORDER_COLOR, highlightthickness=1, borderwidth=0)
    card.pack(fill='x', padx=15, pady=(5, 10))

    # --- 1. Título e Proprietário ---
    title_frame = tk.Frame(card, bg=PROJECT_FRAME_BG)
    title_frame.pack(fill='x', pady=(0, 5))
    
    tk.Label(title_frame, text=project_data["title"], 
             font=font_roboto_big, bg=PROJECT_FRAME_BG, fg=colors["fg_text"], 
             anchor="w").pack(side="left", fill="x", expand=True)

    tk.Label(title_frame, text=f"@{project_data['owner']}", 
             font=font_inter, bg=PROJECT_FRAME_BG, fg=colors["icon_inactive_fg"], 
             anchor="e").pack(side="right")

    # --- 2. Descrição ---
    tk.Label(card, text=project_data["description"], 
             font=font_inter, bg=PROJECT_FRAME_BG, fg=colors["fg_entry"], 
             wraplength=350, justify="left", anchor="w").pack(fill='x', pady=(5, 10))

    # --- 3. Detalhes (Status, Colaboradores, Tech) ---
    details_frame = tk.Frame(card, bg=PROJECT_FRAME_BG)
    details_frame.pack(fill='x', pady=(5, 0))

    # Função auxiliar para criar Labels de detalhes
    def criar_detail_label(parent, key, value, color):
        tk.Label(parent, text=f"{key}: {value}", font=font_inter, 
                 bg=PROJECT_FRAME_BG, fg=color, 
                 anchor="w").pack(side="left", padx=(0, 15))

    # Lógica de cores para o Status
    if project_data["status"] == "Concluído":
        status_color = "#32CD32" # Verde Lima
    elif project_data["status"] == "Em Andamento":
        status_color = "#FFA500" # Laranja
    else:
        status_color = colors["purple_button"] # Roxo padrão
        
    criar_detail_label(details_frame, "Status", project_data["status"], status_color)
    criar_detail_label(details_frame, "Colaboradores", project_data["collaborators"], colors["fg_text"])
    criar_detail_label(details_frame, "Tecnologia", project_data["tech"], colors["fg_text"])
    
    # --- 4. Barra de Progresso (Simples) ---
    progress_val = project_data["progress"]
    progress_frame = tk.Frame(card, bg=PROJECT_FRAME_BG, pady=10)
    progress_frame.pack(fill='x')
    
    # Canvas para a barra de progresso visual
    bar_width = 370 
    progress_bar = tk.Canvas(progress_frame, height=8, width=bar_width, bg=colors["bg_entry"], highlightthickness=0)
    progress_bar.pack(side="left", fill="x", expand=True)
    
    fill_width = (progress_val / 100) * bar_width
    progress_bar.create_rectangle(0, 0, fill_width, 8, fill=colors["purple_button"], outline="")
    
    tk.Label(progress_frame, text=f"{progress_val}%", font=("Inter", 8, "bold"), 
             bg=PROJECT_FRAME_BG, fg=colors["fg_text"], padx=5).pack(side="right")


    return card


def criar_aba_projetos(container_frame, icones): # <-- Ícones agora são um argumento obrigatório
    """
    Cria e retorna o frame principal da aba Projetos (apenas o conteúdo rolável).
    """
    f = tk.Frame(container_frame, bg=colors["bg_main"])
    f.grid_columnconfigure(0, weight=1)

    # Título da Tela
    tk.Label(f, text="Projetos", font=font_roboto_big, bg=colors["bg_main"], fg=colors["fg_text"]).grid(row=0, column=0, pady=(10, 5), sticky="ew")

    # --- Área de Rolagem para a Lista de Projetos ---
    canvas = tk.Canvas(f, bg=colors["bg_main"], highlightthickness=0)
    canvas.grid(row=1, column=0, sticky="nsew", padx=5)
    f.grid_rowconfigure(1, weight=1) 

    scrollbar = tk.Scrollbar(f, orient="vertical", command=canvas.yview, bg=colors["bg_main"])
    scrollbar.grid(row=1, column=1, sticky="ns")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno onde os projetos serão colocados
    projects_frame = tk.Frame(canvas, bg=colors["bg_main"])
    # Largura inicial para o teste
    canvas.create_window((0, 0), window=projects_frame, anchor="nw", width=400) 

    def on_frame_configure(event):
        """Ajusta a região de rolagem do canvas."""
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    projects_frame.bind("<Configure>", on_frame_configure)
    
    def on_canvas_resize(event):
        """Ajusta a largura do frame interno."""
        canvas_width = event.width
        projects_frame.config(width=canvas_width - 20) 
        
    canvas.bind('<Configure>', on_canvas_resize)

    # Popula a lista com os mocks de projetos
    for project in MOCK_PROJECTS_DATA:
        criar_card_projeto(projects_frame, project)

    return f


def criar_bottom_bar(container_frame, icones, current_tab="Projetos"):
    """
    Cria a barra de navegação fixa na parte inferior.
    """
    nav_frame = tk.Frame(container_frame, bg=colors["bottom_bar_bg"], bd=0, relief="flat")
    nav_frame.pack(side="bottom", fill="x", ipady=5)
    nav_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    
    nav_items = ["Home", "Novo Post", "Projetos", "Ranking", "Perfil"]
    
    def on_nav_click(item_name):
        # MOCK: Função para simular a navegação
        messagebox.showinfo("Navegação (Mock)", f"Função para ir para '{item_name}' seria chamada aqui.")

    for i, item_name in enumerate(nav_items):
        icon_image = icones[item_name]
        
        is_active = (item_name == current_tab)
        text_color = colors["icon_active_fg"] if is_active else colors["icon_inactive_fg"]
        
        item_frame = tk.Frame(nav_frame, bg=colors["bottom_bar_bg"])
        item_frame.grid(row=0, column=i, sticky="nsew")
        
        nav_button = tk.Button(item_frame, 
            image=icon_image, 
            command=lambda name=item_name: on_nav_click(name),
            bd=0, 
            relief="flat", 
            bg=colors["bottom_bar_bg"], 
            activebackground=colors["bottom_bar_bg"],
            compound="top" 
        )
        nav_button.image = icon_image 
        nav_button.pack(pady=(5, 2)) 

        label = tk.Label(item_frame, text=item_name, font=("Inter", 8), bg=colors["bottom_bar_bg"], fg=text_color)
        label.pack()


def criar_tela_principal_com_nav(window, icones):
    """
    Cria a estrutura principal (Conteúdo + Bottom Bar).
    """
    # 1. Cria a BARRA INFERIOR (fixa na parte inferior)
    criar_bottom_bar(window, icones, current_tab="Projetos")

    # 2. Cria o frame de CONTEÚDO (ocupa o espaço restante)
    content_frame = tk.Frame(window, bg=colors["bg_main"])
    content_frame.pack(fill="both", expand=True) 
    
    # 3. Adiciona a View de Projetos ao frame de CONTEÚDO
    projects_view = criar_aba_projetos(content_frame, icones) # <-- Ícones são passados aqui
    projects_view.pack(fill="both", expand=True)

# --- BLOCO DE TESTE INDIVIDUAL ---
if __name__ == "__main__":
    # setup_test_window retorna 3 valores: test_window, root, icones_mock
    try:
        test_window, root, icones_mock = setup_test_window("Teste Individual: Aba Projetos") 
        
        # Passa a janela principal e os ícones para a nova função de estrutura
        criar_tela_principal_com_nav(test_window, icones_mock)
        
        root.mainloop()
    except NameError:
        print("ERRO: A função 'setup_test_window' ou outras utilidades não foram encontradas.")
        print("Certifique-se de que o 'utils_icons.py' está no mesmo diretório.")
    except Exception as e:
        # Erro genérico de Tkinter
        print(f"Erro ao iniciar a janela de teste: {e}")