import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import sys
import os
from PIL import Image, ImageTk
import pandas as pd 
from ..data.userData import user_df
from ..service.userService import like_post
from ..service.userService import coment



# MOCK THEME (substitua pelos seus)
DARK_THEME_COLORS = {
    "bg_main": "#1A1A1A",
    "bg_frame": "#2A2A2A",
    "bg_entry": "#333333",
    "fg_text": "#FFFFFF",
    "icon_inactive_fg": "#BBBBBB",
    "purple_button": "#6F42C1"
}

font_inter = ("Inter", 12)


class CommentWindow(tk.Toplevel):
    def __init__(self, master, user_name):
        super().__init__(master)
        self.title("Comentários")
        self.geometry("300x390")
        self.configure(bg="#1A1A1A")

        self.user_name =  user_df[user_df["id"] == user_name]["name"].iloc[0]  # Nome do usuário que vai comentar

        # ========== FRAME PRINCIPAL ==========
        main_frame = tk.Frame(self, bg="#1A1A1A")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ========== ÁREA DOS COMENTÁRIOS (rolável) ==========
        comment_container = tk.Frame(main_frame, bg="#1A1A1A")
        comment_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(comment_container, bg="#1A1A1A", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(comment_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1A1A1A")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Guarda todos os comentários
        self.comments = []

        # ========== ÁREA DE INPUT DO COMENTÁRIO ==========
        input_frame = tk.Frame(main_frame, bg="#1A1A1A")
        input_frame.pack(fill="x", pady=5)

        self.comment_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
        self.comment_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        send_button = tk.Button(
            input_frame,
            text="Enviar",
            command=self.add_comment,
            bg="#6F42C1",
            fg="white",
            font=("Arial", 11, "bold")
        )
        send_button.pack(side="right")

    # ===========================
    # ADICIONA COMENTÁRIO NA TELA
    # ===========================
    def add_comment(self):
        text = self.comment_entry.get().strip()
        coment(self.user_name,text)
        if text == "":
            messagebox.showwarning("Aviso", "Digite um comentário antes de enviar!")
            return

        self.comments.append((self.user_name, text))
        self.comment_entry.delete(0, tk.END)
        self.update_comments()

    # ===========================
    # ATUALIZA VISUALIZAÇÃO
    # ===========================
    def update_comments(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for name, comment in self.comments:
            wrapper = tk.Frame(self.scrollable_frame, bg="#1A1A1A")
            wrapper.pack(fill="x", pady=5)

            # Nome em destaque
            name_label = tk.Label(
                wrapper,
                text=name,
                fg="#6F42C1",
                bg="#1A1A1A",
                font=("Arial", 12, "bold")
            )
            name_label.pack(anchor="w")

            # Comentário embaixo
            comment_label = tk.Label(
                wrapper,
                text=comment,
                fg="white",
                bg="#1A1A1A",
                font=("Arial", 11),
                wraplength=360,
                justify="left"
            )
            comment_label.pack(anchor="w")

        # Mantém scroll sempre no final
        self.canvas.yview_moveto(1)


# --- Importações de Dados e Utils ---

try:
    from redesocial.data.userData import user_df
    from redesocial.data.publicationData import publication_df
    from redesocial.data.midiaData import midia_df
    # Importação de cores e dimensões 
    from redesocial.views.utils_icons import (
        colors, # Embora você use o DARK_THEME, mantive a importação
        font_roboto_big,
        font_roboto,
        font_inter,
        FRAME_WIDTH,
        FRAME_HEIGHT
    )
except ImportError as e:
    
    print(f"Erro ao importar dados/utils: {e}. Usando Mocks de Fallback.")
    
    # Mocks simplificados para o contexto da HomeFeedView
    class MockDataFrame:
        def iterrows(self): return iter([])
        def __len__(self): return 0
        def __getitem__(self, key): return self
        def iloc(self, index): return self
        def isin(self, values): return []
    
    user_df = MockDataFrame()
    publication_df = MockDataFrame()
    midia_df = MockDataFrame()
    
    # Mocks para utils_icons, caso a importação falhe completamente
    class MockColors:
        def __init__(self):
            self.bg_main = "#1e1e1e"
            self.purple_button = "#5653fe"
            self.icon_inactive_fg = "#999999"
    colors = MockColors()
    font_roboto_big = ("Roboto", 16, "bold")
    font_roboto = ("Roboto", 12)
    font_inter = ("Inter", 10)
    FRAME_WIDTH = 420
    FRAME_HEIGHT = 720


# --- Constantes de Tema (Expandidas com a cor da BottomBar) ---
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

# --- FUNÇÃO DE CARREGAMENTO DE ÍCONES (INTEGRADA) ---

# Mapeamento dos nomes lógicos no código para os nomes de arquivo na pasta 'img'
ICON_FILE_MAP = {
    "home_icon": "home_image.png",
    "new_post_icon": "newpost_image.png",
    "projects_icon": "projeto_image.png",
    "ranking_icon": "ranking_image.png",
    "profile_icon": "user_image.png",
    "profile_pic": "profile_pic.png" # Ícone de perfil para o post card
}

def load_navbar_icons(root_window, size=(28, 28)):
    """Carrega ícones da pasta 'img' usando PIL e Tkinter PhotoImage."""
    carregados = {}
    
    # O caminho base é a pasta 'img' dentro da pasta 'views'
    # os.path.dirname(os.path.abspath(__file__)) é a pasta 'views'
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

    for icon_tag, file_name in ICON_FILE_MAP.items():
        full_path = os.path.join(base_path, file_name)
        
        try:
            img = Image.open(full_path)
            
            # Redimensionamento
         
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Converte para PhotoImage, vinculando ao widget mestre
            
            photo = ImageTk.PhotoImage(img, master=root_window) 
            carregados[icon_tag] = photo
            
        except Exception as e:
            # Fallback para o mock
            print(f"ERRO: Não foi possível carregar o ícone '{file_name}'. Erro: {e}")
            carregados[icon_tag] = tk.PhotoImage(width=size[0], height=size[1], master=root_window)
            
    return carregados

# ==========================================================================
# 1. Classe BottomBar (Navbar)
# ==========================================================================
class BottomBar(tk.Frame):
    """Cria a barra de navegação inferior com 5 ícones."""
    
    def __init__(self, master, switch_view_callback, icones, session=None,*args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        bg_frame_color = DARK_THEME_COLORS['bottom_bar_bg']
        icon_inactive_color = DARK_THEME_COLORS['icon_inactive_fg']
        icon_active_color = DARK_THEME_COLORS['icon_active_fg']
        self.session =session
        self.config(bg=bg_frame_color, pady=5)
        self.columnconfigure((0, 1, 2, 3, 4), weight=1) 
        
        self.switch_view_callback = switch_view_callback
        self.icones = icones
        self.buttons = {} 
        self.current_view = tk.StringVar(value="Home") # Variável de estado da View ativa
        
        # Definição dos Itens da Barra
        nav_items = {
            "Home": ("home_icon", "Home", lambda: switch_view_callback("home")), 
            "Novo Post": ("new_post_icon", "Novo Post", lambda: self._show_mock_action("novoprojeto")),
            "Projetos": ("projects_icon", "Projetos", lambda: self._show_mock_action("projects")),
            "Ranking": ("ranking_icon", "Ranking", lambda: self._show_mock_action("ranking")),
            "Perfil": ("profile_icon", "Perfil", lambda: self._show_mock_action("profile")),
        }
        
        col = 0
        for view_name, (icon_tag, text, command) in nav_items.items():
            icon_image = self.icones.get(icon_tag)
            
            # --- Frame para o botão (Ícone + Texto) ---
            btn_frame = tk.Frame(self, bg=bg_frame_color)
            btn_frame.grid(row=0, column=col, sticky='nsew', padx=5)
            
            # --- Ícone ---
            icon_label = tk.Label(btn_frame, 
                                  image=icon_image, 
                                  bg=bg_frame_color)
            icon_label.pack(pady=(2, 0))

            # --- Texto ---
            text_label = tk.Label(btn_frame, 
                                  text=text, 
                                  font=font_inter, 
                                  bg=bg_frame_color)
            text_label.pack(pady=(0, 2))
            
            # Adiciona o comando de clique ao Frame principal
            btn_frame.bind("<Button-1>", lambda e, cmd=command, name=view_name: (self._update_active_state(name),cmd()))
            icon_label.bind("<Button-1>", lambda e, cmd=command, name=view_name: (self._update_active_state(name),cmd()))
            text_label.bind("<Button-1>", lambda e, cmd=command, name=view_name: (self._update_active_state(name),cmd()))

            self.buttons[view_name] = {"frame": btn_frame, "icon": icon_label, "text": text_label}
            col += 1
            
        self._update_active_state(self.current_view.get())
        
    def _update_active_state(self, active_view_name):
        """Atualiza as cores do texto da view ativa."""
        icon_active_color = DARK_THEME_COLORS['icon_active_fg']
        icon_inactive_color = DARK_THEME_COLORS['icon_inactive_fg']
        
        self.current_view.set(active_view_name)
        
        for name, widgets in self.buttons.items():
            is_active = (name == active_view_name)
            color = icon_active_color if is_active else icon_inactive_color
            widgets["text"].config(fg=color)
            
    def _show_mock_action(self, view_name):
        """Ação de callback mock para outras views."""
        
        self.switch_view_callback(view_name) 


# ==========================================================================
# 2. Classe HomeFeedView (Atualizada para incluir Navbar)
# ==========================================================================
class HomeFeedView(tk.Frame):
    """Tela principal de Feed organizada """

    def __init__(self, master, session,switch_view_callback=None, icones=None):
        self.switch_view_callback = switch_view_callback
        self.session = session
        super().__init__(master, bg=DARK_THEME_COLORS["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        print(session)
        print(user_df[user_df["id"] == session])
        # O carregamento dos ícones deve ser feito ANTES de criar a view principal
        self.icones = icones or load_navbar_icons(master) # Fallback para carregar se não vier injetado
        self.pack_propagate(False)
        
        self._create_widgets()
        self._create_bottom_bar() # Chamada para criar a Navbar

    def open_comments(self, post_id):
        """Abre a janela de comentários para o post escolhido."""
        CommentWindow(self, post_id)
            # Obter dados do usuário (usando a lógica do pandas)
    # ---------------------------------------------------------------------
    # 1. Criar estrutura da tela (Header e Content Area)
    # ---------------------------------------------------------------------
    def _create_widgets(self):
        
        # ---------- Cabeçalho ----------
        header = tk.Frame(self, bg=DARK_THEME_COLORS["bg_frame"], pady=10)
        header.pack(fill='x', side=tk.TOP) # Empacota no topo

        tk.Label(header,
                 text="MIAU",
                 font=("Inter", 18, "bold"),
                 bg=DARK_THEME_COLORS["bg_frame"],
                 fg=DARK_THEME_COLORS["purple_button"]).pack()

        # ---------- Área Rolável (Content Area) ----------
        # Frame intermediário que vai expandir entre o Header e a BottomBar
        content_wrapper = tk.Frame(self, bg=DARK_THEME_COLORS["bg_main"])
        content_wrapper.pack(side=tk.TOP, fill="both", expand=True) # Expande no meio

        self.canvas = tk.Canvas(content_wrapper, bg=DARK_THEME_COLORS["bg_main"], highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(content_wrapper, orient='vertical', command=self.canvas.yview)

        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.feed_frame = tk.Frame(self.canvas, bg=DARK_THEME_COLORS["bg_main"])
        self.canvas_window = self.canvas.create_window((0, 0),
                                                       window=self.feed_frame,
                                                       anchor="nw",
                                                       width=FRAME_WIDTH)

        # eventos de atualização
        self.feed_frame.bind("<Configure>", self._update_scroll)
        self.canvas.bind("<Configure>", self._update_scroll)

        # carrega posts
        self._load_feed()


    # ---------------------------------------------------------------------
    # 2. Criar BottomBar (Navbar)
    # ---------------------------------------------------------------------
    def _create_bottom_bar(self):
        """Cria e empacota a BottomBar na parte inferior da HomeFeedView."""
        
        # O self.master (o root/toplevel) é o mestre da BottomBar
        self.bottom_bar = BottomBar(
            self, # Coloca a barra DENTRO da HomeFeedView
            self.switch_view_callback,
            self.icones,
            bg=DARK_THEME_COLORS["bottom_bar_bg"],
            session = self.session
        )
        # Empacota no fundo da HomeFeedView (que é a própria self)
        self.bottom_bar.pack(fill="x", side=tk.BOTTOM) 


    # ---------------------------------------------------------------------
    def _update_scroll(self, event):
        """Mantém o scroll sempre correto."""
        # Se o evento for no self.canvas, ajusta a largura da janela de conteúdo
        if event.widget == self.canvas:
             self.canvas.itemconfig(self.canvas_window, width=event.width)

        # Ajusta a região de scroll
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # ---------------------------------------------------------------------
    # 3. Montar o Feed
    # ---------------------------------------------------------------------
    def _load_feed(self):
        """Itera o DataFrame e cria cada card."""
        # Garante que o DataFrame não está mockado como MockDataFrame vazio
        if isinstance(publication_df, pd.DataFrame) or publication_df.__len__() > 0:
            for _, post in publication_df.iterrows():
                self._create_post_card(post)
        else:
            tk.Label(self.feed_frame, text="Nenhuma publicação encontrada.",
                     bg=DARK_THEME_COLORS["bg_main"], fg=DARK_THEME_COLORS["icon_inactive_fg"]).pack(pady=20)

    
    # ---------------------------------------------------------------------
    # 4. Criar o card individual
    # ---------------------------------------------------------------------
    def _create_post_card(self, post_data):
        """Cria um post no mesmo estilo da versão anterior, só que organizado."""
        card = tk.Frame(self.feed_frame, bg=DARK_THEME_COLORS["bg_frame"], padx=15, pady=15)
        card.pack(fill='x', padx=10, pady=10)
    
        try:
            username = user_df[user_df["id"] == post_data["user"]]["name"].iloc[0]
        except (IndexError, KeyError):
            username = "Usuário Desconhecido"
            
        text = post_data["description"]
        timestamp = f"{post_data['day']} {post_data['times']}"

        # ---------- Cabeçalho ----------
        tk.Label(card,
                 text=username,
                 font=font_roboto_big,
                 bg=DARK_THEME_COLORS["bg_frame"],
                 fg=DARK_THEME_COLORS["fg_text"]).pack(anchor='w')

        tk.Label(card,
                 text=timestamp,
                 font=font_inter,
                 bg=DARK_THEME_COLORS["bg_frame"],
                 fg=DARK_THEME_COLORS["icon_inactive_fg"]).pack(anchor='w')

        # ---------- Texto ----------
        tk.Label(card,
                 text=text,
                 font=font_roboto,
                 bg=DARK_THEME_COLORS["bg_frame"],
                 fg=DARK_THEME_COLORS["fg_text"],
                 wraplength=FRAME_WIDTH - 60,
                 justify='left').pack(anchor='w', pady=10)

        # ---------- Imagem ----------
        self._add_post_image(card, post_data)
        def like(id_post,id_user):
            
            like_post(id_post,id_user)
            self.switch_view_callback("home")
          
        # ---------- Ações ----------
        actions = tk.Frame(card, bg=DARK_THEME_COLORS["bg_frame"])
        actions.pack(fill='x', pady=5)
        id_user = user_df[user_df["id"] == self.session]["id"].iloc[0]
        id_post = post_data["id"]
        tk.Button(actions, text=f"❤️ {publication_df[publication_df["id"] == id_post]["like_counter"].iloc[0]}",
                  
                  bg=DARK_THEME_COLORS["bg_frame"],
                  fg=DARK_THEME_COLORS["icon_inactive_fg"],
                  bd=0,
                  command= lambda:like(id_post,id_user),
                  font=font_inter).pack(side='left', padx=10)
        pid = post_data["id"]
        tk.Button(actions, text="💬 Comentar",
                  bg=DARK_THEME_COLORS["bg_frame"],
                  fg=DARK_THEME_COLORS["icon_inactive_fg"],
                  bd=0,
                  command= lambda:  self.open_comments(pid),
                  font=font_inter).pack(side='left')
        
    
    # ---------------------------------------------------------------------
    def _add_post_image(self, parent, post_data):
        """Carrega imagem se existir."""
        # Garante que 'midia_list' existe
        if "midia_list" not in post_data or not post_data["midia_list"]:
             return

        midias_ids = [m["id"] for m in post_data["midia_list"]]
        midias_do_post = midia_df[midia_df["id"].isin(midias_ids)]

        if len(midias_do_post) == 0:
            return

        image_path = midias_do_post.iloc[0]["original_path"]

        try:
            img = Image.open(image_path)
            # Resampling.LANCZOS é a opção de alta qualidade no PIL 9+
            img = img.resize((350, 350), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(img, master=parent)
            parent.photo = photo

            tk.Label(parent, image=photo, bg=DARK_THEME_COLORS["bg_frame"]).pack(pady=10)
        except Exception as e:
            print("Erro carregando imagem:", e)


