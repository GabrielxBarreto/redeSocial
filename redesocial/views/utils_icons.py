import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import tkinter.font as tkFont 
import os
import sys
from tkinter import messagebox

# ==============================================================================
# 1. CONSTANTES E CORES
# ==============================================================================

DARK_THEME_COLORS = {
    "bg_main": "#1e1e1e",
    "bg_frame": "#252526",
    "bg_entry": "#333333",
    "fg_text": "#ffffff",
    "fg_entry": "#d4d4d4",
    "bg_button": "#555555",
    "active_bg_button": "#666666",
    "purple_button": "#5653fe", 
    "bottom_bar_bg": "#1e1e1e", # Cor específica para a barra de navegação
    "icon_active_fg": "#5653fe",
    "icon_inactive_fg": "#999999",
}
colors = DARK_THEME_COLORS

# Fontes - Definidas como tuplas de string (seguras na importação)
font_inter_small = ("Inter", 10)
font_roboto = ("Roboto", 12)
font_inter = ("Inter", 10)
font_roboto_big = ("Roboto", 16, "bold")

# Constantes de Tamanho
ICON_SIZE_NAV = (30, 30)
FRAME_WIDTH = 420
FRAME_HEIGHT = 720
BOTTOM_BAR_HEIGHT = 60 # Altura fixa para a barra de navegação


# ==============================================================================
# 2. MOCKS DE DADOS E FUNÇÕES DE CONTROLLER
# ==============================================================================

MOCK_PROFILE_DATA = {
    "username": "TesteUsuario",
    "bio": "Desenvolvedor em treinamento no IFC. Apaixonado por Python e Tkinter!",
    "location": "Concórdia - SC",
    "education": "IFC Concórdia",
    "interests": ["Python", "Tkinter", "UX/UI Design", "Algoritmos"],
    "posts": [
        {"text": "Meu primeiro post na rede social! Que venham muitos projetos.", "has_image": False},
        {"text": "Consegui resolver um bug chato com as imports relativas hoje. Vitória!", "has_image": True},
        {"text": "Estudando como funciona a persistência de dados em aplicações.", "has_image": False},
    ]
}

MOCK_FEED_POSTS = [
    {"user": "Alice", "text": "Adorei a nova biblioteca de visualização de dados!", "has_image": False, "profile_pic": "profile_pic.png"},
    {"user": "Bob", "text": "Projeto final quase pronto. Muita cafeína envolvida!", "has_image": True, "profile_pic": "friends_icon.png"},
    {"user": "papai.dev", "text": "Melhorando a interface com Tkinter! Design responsivo. Melhorando a interface com Tkinter! Design responsivo. Melhorando a interface com Tkinter! Design responsivo.", "has_image": False, "profile_pic": "user_image.png"},
    {"user": "User4", "text": "Mais um dia de commits! Foco na entrega.", "has_image": False, "profile_pic": "friends_icon.png"},
    {"user": "User5", "text": "Testando as novas funcionalidades de AI. Impressionante!", "has_image": True, "profile_pic": "user_image.png"},
    {"user": "User6", "text": "Passei no teste de lógica! Que sensação boa.", "has_image": False, "profile_pic": "friends_icon.png"},
    {"user": "User7", "text": "Planejando o próximo sprint.", "has_image": False, "profile_pic": "profile_pic.png"},
    {"user": "User8", "text": "Aprendendo sobre padrões de projeto.", "has_image": True, "profile_pic": "user_image.png"},
]

# DADOS DE MOCK PARA A TELA DE RANKING (Adicionado para esta nova view)
MOCK_RANKING_DATA = [
    {"rank": 1, "username": "AliceDev", "points": 1250, "projects": 5},
    {"rank": 2, "username": "BobCoder", "points": 980, "projects": 3},
    {"rank": 3, "username": "papai.dev", "points": 850, "projects": 4},
    {"rank": 4, "username": "CarolTech", "points": 720, "projects": 2},
    {"rank": 5, "username": "DanJunior", "points": 600, "projects": 1},
    {"rank": 6, "username": "EveCode", "points": 510, "projects": 3},
    {"rank": 7, "username": "FrankPython", "points": 450, "projects": 2},
    {"rank": 8, "username": "GraceJS", "points": 390, "projects": 1},
    {"rank": 9, "username": "Henry", "points": 300, "projects": 1},
    {"rank": 10, "username": "Ivy", "points": 250, "projects": 2},
]


def load_user_profile_data(usuario):
    """MOCK: Carrega os dados do usuário (retorna dados estáticos)."""
    return MOCK_PROFILE_DATA

def update_user_bio(usuario, nova_bio):
    """MOCK: Atualiza a Bio do usuário no mock de dados."""
    MOCK_PROFILE_DATA["bio"] = nova_bio
    messagebox.showinfo("Sucesso", "Descrição salva (Mock).")

def update_user_interests(usuario, novos_interesses):
    """MOCK: Atualiza a lista de interesses no mock de dados."""
    MOCK_PROFILE_DATA["interests"] = novos_interesses
    messagebox.showinfo("Sucesso", "Interesses atualizados (Mock).")

def dummy_navigation_command(view_name):
    """Função de mock para simular a navegação entre telas."""
    print(f"Navegar para a view: {view_name}")


# ==============================================================================
# 3. FUNÇÕES DE CARREGAMENTO DE ÍCONE E MOCK
# ==============================================================================

# Assumindo que a pasta 'img' está no mesmo diretório das views para o teste.
# NOTA: O ambiente Canvas não tem a pasta 'img', então dependemos dos mocks.
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img") 

def hex_to_rgba(hex_color, alpha=255):
    """Converte uma string de cor hexadecimal (#RRGGBB) para uma tupla RGBA (R, G, B, A)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b, alpha)

def create_placeholder_icon(size, color=None, is_nav=False, shape="square", draw_icon_shape=None):
    """
    Gera uma imagem placeholder em memória (quadrado sólido) para garantir PhotoImage válido.
    Adicionado argumento 'shape' para customizar o placeholder.
    """
    
    # Determinar a cor de preenchimento
    if color is None or color == "gray":
        fill_color = hex_to_rgba(colors["icon_inactive_fg"])
    elif color == "red":
        fill_color = (255, 0, 0, 255) # Placeholder de erro
    elif color == colors["icon_active_fg"]:
        fill_color = hex_to_rgba(colors["icon_active_fg"])
    elif color == "#333333": # Cor de fundo para profile pic
        fill_color = hex_to_rgba(color)
    else: # Default para fundo (e.g., cover image)
        fill_color = hex_to_rgba(colors["bg_frame"])
        
    try:
        img = Image.new('RGBA', size, fill_color)
        draw = ImageDraw.Draw(img)
        
        # Desenha formas customizadas para melhor visualização dos mocks
        if shape == "circle":
             draw.ellipse([(0, 0), (size[0], size[1])], fill=fill_color)
        elif shape == "rounded_rect":
             radius = min(size) // 8
             draw.rounded_rectangle([(0, 0), (size[0], size[1])], radius=radius, fill=fill_color)
        
        # Desenha uma forma interna se draw_icon_shape for fornecido
        if draw_icon_shape:
             draw_inner_icon(draw, size, draw_icon_shape, hex_to_rgba(colors["fg_text"]))
             
        return ImageTk.PhotoImage(img)
    except Exception:
        # Fallback se a inicialização do PIL/Tkinter falhar
        return None

def draw_inner_icon(draw, size, shape, color):
    """Desenha uma forma interna simples para ícones de navegação."""
    w, h = size
    
    if shape == "home":
        # Simula uma casa (Home)
        draw.rectangle([w*0.3, h*0.5, w*0.7, h*0.8], fill=color)
        draw.polygon([w*0.2, h*0.5, w*0.5, h*0.2, w*0.8, h*0.5], fill=color)
    elif shape == "plus":
        # Simula um sinal de mais (Novo Post)
        draw.rectangle([w*0.4, h*0.2, w*0.6, h*0.8], fill=color)
        draw.rectangle([w*0.2, h*0.4, w*0.8, h*0.6], fill=color)
    elif shape == "projects":
        # Simula um livro ou pasta (Projetos)
        draw.rectangle([w*0.3, h*0.3, w*0.7, h*0.7], outline=color, width=2)
        draw.line([w*0.7, h*0.3, w*0.8, h*0.2], fill=color, width=2)
        draw.line([w*0.8, h*0.2, w*0.8, h*0.6], fill=color, width=2)
        draw.line([w*0.7, h*0.7, w*0.8, h*0.6], fill=color, width=2)
    elif shape == "ranking":
        # Simula um troféu (Ranking)
        draw.rectangle([w*0.4, h*0.7, w*0.6, h*0.8], fill=color)
        draw.ellipse([w*0.3, h*0.3, w*0.7, h*0.7], fill=color)
        draw.rectangle([w*0.45, h*0.2, w*0.55, h*0.3], fill=color)
    elif shape == "user":
        # Simula um usuário (Perfil)
        draw.ellipse([w*0.35, h*0.25, w*0.65, h*0.55], fill=color)
        draw.arc([w*0.1, h*0.5, w*0.9, h*0.9], start=20, end=160, fill=color, width=3)


def carregar_icone(nome_arquivo, tamanho):
    """Tenta carregar o ícone, usa placeholder como fallback."""
    
    color = colors["icon_inactive_fg"]
    shape = "square"
    draw_shape = None
    
    if "profile_pic" in nome_arquivo:
        color = "#333333" # Cor mais escura para a foto de perfil
        shape = "circle"
    elif "cover_image" in nome_arquivo:
        color = colors["bg_frame"] # Cor de fundo mais clara para a capa
        shape = "rounded_rect"
    elif "post_image" in nome_arquivo:
        color = colors["bg_frame"] # Imagem de post
        shape = "rounded_rect"
    
    # Mapeamento para ícones de navegação
    elif "home_image" in nome_arquivo:
        draw_shape = "home"
    elif "newpost_image" in nome_arquivo:
        draw_shape = "plus"
    elif "projeto_image" in nome_arquivo:
        draw_shape = "projects"
    elif "ranking_image" in nome_arquivo:
        draw_shape = "ranking"
    elif "user_image" in nome_arquivo:
        draw_shape = "user"

    # Para todos os ícones que não são fotos/capas, desenha a forma interna
    return create_placeholder_icon(tamanho, color=color, shape=shape, draw_icon_shape=draw_shape)


# --- MOCKS DOS ÍCONES USADOS NA APLICAÇÃO ---

def carregar_icones_mock():
    """Função para carregar os ícones APENAS DEPOIS que o Tkinter estiver inicializado."""
    return {
        # Ícones de Navegação
        "Home": carregar_icone("home_image.png", tamanho=ICON_SIZE_NAV),
        "Novo Post": carregar_icone("newpost_image.png", tamanho=ICON_SIZE_NAV),
        "Projetos": carregar_icone("projeto_image.png", tamanho=ICON_SIZE_NAV),
        "Ranking": carregar_icone("ranking_image.png", tamanho=ICON_SIZE_NAV),
        "Perfil": carregar_icone("user_image.png", tamanho=ICON_SIZE_NAV),
        
        # Ícones de Perfil/Feed
        "cover_image": carregar_icone("cover_image.png", tamanho=(FRAME_WIDTH, 150)),
        "profile_pic_feed": carregar_icone("profile_pic.png", tamanho=(40, 40)), # Menor para o feed
        "profile_pic_user": carregar_icone("profile_pic_user.png", tamanho=(80, 80)), # Maior para o perfil
        "back_arrow": carregar_icone("back_arrow.png", tamanho=(24, 24)),
        "friends_icon": carregar_icone("friends_icon.png", tamanho=(20, 20)),
        "location_icon": carregar_icone("location_icon.png", tamanho=(16,16)),
        "education_icon": carregar_icone("education_icon.png", tamanho=(16,16)),
        "post_image": carregar_icone("post_image.png", tamanho=(FRAME_WIDTH - 40, 200)), # Ajustado para caber no frame
        
        # Ícones de interação no post (mocks simples)
        "like_icon": carregar_icone("like_icon.png", tamanho=(24, 24)),
        "comment_icon": carregar_icone("comment_icon.png", tamanho=(24, 24)),
        "share_icon": carregar_icone("share_icon.png", tamanho=(24, 24)),
    }


# --- FUNÇÃO AUXILIAR PARA TESTE INDIVIDUAL ---
def setup_test_window(title="Teste de Tela"):
    """
    Cria e retorna a janela Toplevel, a raiz (root) e o dicionário de ícones.
    """
    root = tk.Tk()
    root.withdraw() # Esconde a janela raiz
    test_window = tk.Toplevel(root)
    test_window.title(title)
    test_window.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}")
    test_window.resizable(False, False)
    test_window.config(bg=colors["bg_main"])

    # CHAMA A FUNÇÃO DE CARREGAR ÍCONES AGORA QUE TKINTER ESTÁ PRONTO
    icones_carregados = carregar_icones_mock()
    
    # Armazena referências de imagens para evitar GC
    test_window.image_refs = list(icones_carregados.values()) 
    
    # Função para fechar a janela corretamente
    def on_closing():
        test_window.destroy()
        root.quit()
        
    test_window.protocol("WM_DELETE_WINDOW", on_closing)
    return test_window, root, icones_carregados # <-- Retornando 3 valores!

# ==============================================================================
# 4. COMPONENTE DE BARRA INFERIOR (BottomBar) - Implementação para corrigir o erro
# ==============================================================================

class BottomBar(tk.Frame):
    """
    Barra de navegação inferior que alterna entre views.
    """
    def __init__(self, master, switch_view_callback, icones, current_view_state, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.switch_view_callback = switch_view_callback
        self.icones = icones
        self.current_view_state = current_view_state
        
        self.config(
            bg=colors["bottom_bar_bg"], 
            height=BOTTOM_BAR_HEIGHT, 
            bd=0,
            relief=tk.FLAT
        )
        self.pack_propagate(False) # Garante que o frame mantenha a altura
        
        # Mapeamento dos botões: (Nome do Ícone no dicionário, Nome da View para Callback)
        self.views = [
            ("Home", "Home"), 
            ("Novo Post", "NewPost"), 
            ("Projetos", "Projetos"), 
            ("Ranking", "Ranking"), 
            ("Perfil", "Perfil")
        ]
        
        # Dicionário para armazenar referências aos botões
        self.button_widgets = {} 
        
        self._create_widgets()
        
        # Monitora a mudança de view para atualizar a cor do ícone
        self.current_view_state.trace_add("write", self._update_icon_colors)


    def _create_widgets(self):
        """Cria os botões da barra inferior."""
        
        for icon_name_display, view_name_callback in self.views:
            icon = self.icones.get(icon_name_display)
            
            # Frame container para cada botão
            btn_container = tk.Frame(self, bg=colors["bottom_bar_bg"], width=FRAME_WIDTH // len(self.views))
            btn_container.pack(side=tk.LEFT, fill='y', expand=True)

            # Botão de ícone
            button = tk.Button(
                btn_container,
                image=icon,
                text=icon_name_display, 
                compound=tk.TOP, 
                command=lambda name=view_name_callback: self._on_click(name),
                bg=colors["bottom_bar_bg"],
                bd=0,
                activebackground=colors["bottom_bar_bg"],
                fg=colors["icon_inactive_fg"], # Cor inicial
                activeforeground=colors["icon_active_fg"],
                font=font_inter_small,
                cursor="hand2"
            )
            button.pack(expand=True)
            
            # Armazena a referência para o botão (chave: nome da view)
            self.button_widgets[view_name_callback] = button
            
            # Necessário para evitar o Garbage Collector
            button.image = icon 
            
            # Adiciona o botão ao container para referenciar (necessário para o layout)
            btn_container.button = button 


        # Faz a primeira atualização de cores
        self._update_icon_colors()


    def _on_click(self, view_name):
        """Manipulador de clique que atualiza o estado e chama o callback de navegação."""
        self.current_view_state.set(view_name)
        self.switch_view_callback(view_name)


    def _update_icon_colors(self, *args):
        """
        Atualiza a cor dos ícones baseado na view ativa.
        Lógica simplificada e corrigida.
        """
        active_view = self.current_view_state.get()
        
        for view_name, button in self.button_widgets.items():
            if active_view == view_name:
                # View Ativa: Cor Roxo/Azul
                button.config(fg=colors["icon_active_fg"])
            else:
                # View Inativa: Cor Cinza
                button.config(fg=colors["icon_inactive_fg"])

# ==============================================================================
# TESTE DE EXECUÇÃO INDIVIDUAL
# ==============================================================================
if __name__ == "__main__":
    
    test_window, root, icones = setup_test_window("Teste do Utils e BottomBar")
    
    # Adiciona a BottomBar
    current_view_state = tk.StringVar(value="Home")
    
    # Callback de mock para a navegação
    def mock_switch_view(view_name):
        print(f"DEBUG: Navegação acionada -> {view_name}")
        # A cor será atualizada automaticamente via trace_add
        
    bottom_bar = BottomBar(
        test_window, 
        mock_switch_view, 
        icones, 
        current_view_state
    )
    bottom_bar.pack(side=tk.BOTTOM, fill="x")
    
    # Adiciona um rótulo no centro para mostrar a view atual
    central_label = tk.Label(test_window, 
                             text=f"View Atual: {current_view_state.get()}", 
                             font=font_roboto_big, 
                             bg=colors["bg_main"], 
                             fg=colors["fg_text"])
    central_label.pack(expand=True)
    
    # Atualiza o rótulo quando a view muda
    current_view_state.trace_add("write", lambda *args: central_label.config(text=f"View Atual: {current_view_state.get()}"))

    print("Clique nos botões da barra inferior. O rótulo e a cor do ícone devem mudar.")
    
    test_window.mainloop()