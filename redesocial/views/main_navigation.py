import tkinter as tk
import sys
import os
from tkinter import messagebox

# ==============================================================================
# CONFIGURAÇÃO DE IMPORTS E MOCKS (CRÍTICO PARA EXECUÇÃO ISOLADA)
# ==============================================================================

# Adiciona o diretório raiz 'redesocial' ao PATH para imports absolutos no teste
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
except:
    pass # Permite que o script continue mesmo se o path não for encontrado

def _get_config_and_views():
    """Tenta carregar as configurações e views do pacote. Usa Mocks se falhar."""
    try:
        from redesocial.config.settings import DARK_THEME_COLORS, inicializar_fontes, carregar_icone, font_roboto, font_inter
        from .home_feed_view import create_home_content
        from .ranking_view import create_ranking_content
        from .projects_view import create_projects_content
        from .user_profile_view import create_profile_content
        return {
            "colors": DARK_THEME_COLORS,
            "fonts": {"roboto": font_roboto, "inter": font_inter},
            "initializers": {"init_fonts": inicializar_fontes, "load_icon": carregar_icone},
            "views": {
                "Home": create_home_content,
                "Ranking": create_ranking_content,
                "Projetos": create_projects_content,
                "Perfil": create_profile_content
            }
        }
    except ImportError as e:
        print(f"Aviso: Não foi possível carregar o pacote completo. Usando Mocks. Erro: {e}")
        
        # Mocks para Configurações
        MOCK_COLORS = {
            "bg_main": "#1e1e1e", "bg_frame": "#2e2e2e", "bg_secondary": "#3e3e3e",
            "fg_text": "#f0f0f0", "purple_button": "#6a0dad", "fg_button": "#ffffff", 
            "icon_active_fg": "#ffcc00", "icon_inactive_fg": "#999999", "bottom_bar_bg": "#1e1e1e",
        }
        def mock_init_fonts(): pass
        def mock_load_icon(path, tamanho=None): return None 
        
        # Mocks para Views (Funções que apenas exibem texto)
        def mock_content(container, user, colors, fonts, icons, callback):
            tk.Label(container, text=f"Conteúdo de {container.name}", font=("Arial", 20, "bold"), 
                     bg=colors["bg_frame"], fg=colors["fg_text"], pady=50).pack(expand=True, fill="both")

        return {
            "colors": MOCK_COLORS,
            "fonts": {"roboto": ("Arial", 12), "inter": ("Arial", 10)},
            "initializers": {"init_fonts": mock_init_fonts, "load_icon": mock_load_icon},
            "views": {
                "Home": mock_content, "Ranking": mock_content, 
                "Projetos": mock_content, "Perfil": mock_content
            }
        }

# ==============================================================================
# ESTRUTURA PRINCIPAL DA APLICAÇÃO (APP SHELL)
# ==============================================================================

def abrir_main_app(usuario, login_root=None):
    """
    Cria a janela principal (Toplevel) e a barra de navegação, 
    e gerencia a exibição das diferentes views de conteúdo.
    """
    
    # 1. Carrega as configurações e views
    config = _get_config_and_views()
    colors = config["colors"]
    init_fonts = config["initializers"]["init_fonts"]
    load_icon = config["initializers"]["load_icon"]
    views = config["views"]
    
    # Inicializa fontes
    init_fonts()
    
    # Oculta a janela de login se existir
    if login_root:
        login_root.withdraw() 
    
    # 2. Criação da Janela Home
    app_shell = tk.Toplevel(login_root, bg=colors["bg_main"])
    app_shell.title("Rede Social - Principal")
    app_shell.geometry("800x600")
    app_shell.minsize(400, 500)
    
    # Mock de dados do usuário (serão passados para todas as views)
    profile_data = {"username": usuario, "bio": "Minha bio inicial", "interests": ["Tech", "Code"]}
    
    # Ícones para a barra de navegação
    icones_bar = {
        "Home": load_icon("home.png", tamanho=(24, 24)),
        "Ranking": load_icon("ranking.png", tamanho=(24, 24)),
        "Projetos": load_icon("project.png", tamanho=(24, 24)),
        "Perfil": load_icon("profile.png", tamanho=(24, 24)),
    }
    
    abas_principais = ["Home", "Ranking", "Projetos", "Perfil"]
    # Frames de Conteúdo: Onde cada view será empacotada
    content_frames = {} 
    botoes_barra = []
    
    # 3. Frame do Conteúdo (acima da barra inferior)
    content_area = tk.Frame(app_shell, bg=colors["bg_main"])
    content_area.pack(fill="both", expand=True)
    
    def fazer_logout():
        """Função de Logout."""
        app_shell.destroy()
        if login_root:
            login_root.deiconify()
        messagebox.showinfo("Logout", "Sessão encerrada com sucesso.")
        
    def mostrar_aba_principal(aba):
        """Alterna a exibição da aba principal e atualiza o estilo dos botões."""
        for fr in content_frames.values(): fr.pack_forget()
        
        # O frame de conteúdo específico é recriado e empacotado
        content_frames[aba].pack(fill="both", expand=True)
        
        for btn in botoes_barra:
            is_active = btn.cget("text") == aba
            btn.config(fg=colors["icon_active_fg"] if is_active else colors["icon_inactive_fg"],
                        activeforeground=colors["icon_active_fg"] if is_active else colors["icon_inactive_fg"])

    # 4. Criação dos Frames de Conteúdo e Chamada das Views
    for aba in abas_principais:
        # Cria o frame container para a view
        frame = tk.Frame(content_area, bg=colors["bg_main"])
        frame.name = aba # Adiciona um nome para fins de debug/mock
        content_frames[aba] = frame
        
        # Limpa o frame para evitar duplicação de widgets ao trocar
        for widget in frame.winfo_children(): widget.destroy()

        # Chama a função de criação da View (importada)
        if aba in views:
            views[aba](frame, profile_data, colors, config["fonts"], icones_bar, mostrar_aba_principal)
        else:
             tk.Label(frame, text=f"Erro: View '{aba}' não encontrada.", bg=colors["bg_main"], fg=colors["fg_text"]).pack()

    # 5. Barra de Navegação Inferior
    barra = tk.Frame(app_shell, bg=colors["bottom_bar_bg"], height=60, relief="flat", bd=0, padx=5, pady=5)
    barra.pack(side="bottom", fill="x")

    for aba in abas_principais:
        icone = icones_bar.get(aba)
        btn = tk.Button(barra, text=aba, image=icone, compound='top', width=60, 
                        command=lambda a=aba: mostrar_aba_principal(a), 
                        font=config["fonts"]["inter"], bd=0, highlightthickness=0, 
                        bg=colors["bottom_bar_bg"], 
                        activebackground=colors["bottom_bar_bg"], 
                        activeforeground=colors["purple_button"])
        
        btn.pack(side="left", expand=True, fill="x", padx=5)
        botoes_barra.append(btn) 

    # Garante que os ícones fiquem na memória
    app_shell.image_refs = list(icones_bar.values()) 
    
    # Inicia a tela na aba Home
    mostrar_aba_principal("Home")
    
    # Lidar com o fechamento da janela
    app_shell.protocol("WM_DELETE_WINDOW", lambda: on_closing(app_shell, login_root))
    
    app_shell.mainloop()

def on_closing(root, login_root):
    """Fecha a aplicação ou volta para a tela de login."""
    if login_root:
        root.destroy()
        login_root.deiconify()
    else:
        root.destroy()
        
# Bloco de teste para execução isolada
if __name__ == "__main__":
    # Cria uma raiz para simular a janela de login
    test_root = tk.Tk()
    test_root.withdraw() 
    
    # Chama a tela principal com um usuário mockado
    abrir_main_app("UsuarioDeTeste", test_root)