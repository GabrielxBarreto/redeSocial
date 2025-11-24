import tkinter as tk
from tkinter import ttk
if __package__:
    from redesocial.data.userData import user_df
    from redesocial.data.publicationData import publication_df

else:
    
    from redesocial.data.publicationData import publication_df

import sys
import os

# Importa as utilidades do arquivo pai (utils_icons.py)
# NOTA: Assumimos que utils_icons.py está no mesmo diretório ou em um caminho de módulo acessível
try:
    from redesocial.views.utils_icons import (
        colors, 
        font_roboto_big, 
        font_roboto, 
        font_inter, 
        FRAME_WIDTH, 
        FRAME_HEIGHT, 
        MOCK_FEED_POSTS, 
        carregar_icones_mock, 
        setup_test_window
    )
except ImportError:
    # Fallback para execução local ou ambiente de teste
    print("Erro ao importar utilidades. Verifique se 'utils_icons.py' está no caminho correto.")
    
    # Mocks MÍNIMOS para evitar quebras no teste unitário
    class MockColors:
        bg_main = "#1e1e1e"
        bg_frame = "#252526"
        bg_entry = "#333333"
        fg_text = "#ffffff"
        purple_button = "#5653fe"
        icon_active_fg = "#5653fe"
        icon_inactive_fg = "#999999" # Adicionado para completar o mock
    colors = MockColors()
    font_roboto_big = ("Roboto", 16, "bold")
    font_roboto = ("Roboto", 12)
    font_inter = ("Inter", 10)
    FRAME_WIDTH = 420
    FRAME_HEIGHT = 720
    MOCK_FEED_POSTS = [
        {"user": "MockUser1", "text": "Post de teste 1.", "has_image": False},
        {"user": "MockUser2", "text": "Post de teste 2 com imagem.", "has_image": True},
    ]
    def setup_test_window(*args): 
        root = tk.Tk()
        root.withdraw()
        window = tk.Toplevel(root)
        window.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}")
        return window, root, {}
    def carregar_icones_mock(): return {}


# ==========================================================================
# 1. Componente Card do Post
# ==========================================================================
def create_post_card(parent, post_data, icones):
    """Cria um cartão de post individual para o feed."""
    print("começou!!")
    global id
    global user
    global description
    global day_time
    id_to_name = dict(zip(user_df["id"], user_df["name"]))
    for _, row in publication_df.iterrows():
        username = row["user"]              # o ID do user
        user= id_to_name.get(username, "Usuário não encontrado")
        print(user, "publicou:", row["description"])


        id = row["id"]
        description = row["description"]
        day_time = row["day"] +" "+row["times"]
    
# Frame principal do post
    # Certifique-se de que colors é um dicionário ou objeto acessível por chave
    bg_frame_color = colors.bg_frame if hasattr(colors, 'bg_frame') else colors["bg_frame"]
    fg_text_color = colors.fg_text if hasattr(colors, 'fg_text') else colors["fg_text"]
    icon_inactive_color = colors.icon_inactive_fg if hasattr(colors, 'icon_inactive_fg') else colors["icon_inactive_fg"]
    bg_entry_color = colors.bg_entry if hasattr(colors, 'bg_entry') else colors["bg_entry"]
    purple_button_color = colors.purple_button if hasattr(colors, 'purple_button') else colors["purple_button"]

    card_frame = tk.Frame(parent, bg=bg_frame_color, padx=15, pady=15)
    card_frame.pack(fill='x', padx=10, pady=(5, 10))
    card_frame.columnconfigure(1, weight=1) # Faz a coluna do nome de usuário expandir
    
    # Ícone de Perfil (Mock)
    profile_pic_mock = icones.get("profile_pic")
    if profile_pic_mock:
        # Usamos um Frame interno para garantir o alinhamento e padding
        profile_frame = tk.Frame(card_frame, bg=bg_frame_color)
        profile_frame.grid(row=0, column=0, rowspan=2, sticky='n', padx=(0, 10))
        
        tk.Label(profile_frame, 
                 image=profile_pic_mock, 
                 bg=bg_frame_color,
                 width=30, height=30).pack()
    
    # Nome de Usuário
    username_label = tk.Label(card_frame, 
                              text=user, 
                              font=font_roboto_big, 
                              bg=bg_frame_color, 
                              fg=fg_text_color,
                              anchor='w')
    username_label.grid(row=0, column=1, sticky='ew')
    
    # Data/Hora do Post (Mock)
    time_label = tk.Label(card_frame, 
                          text=day_time, 
                          font=font_inter, 
                          bg=bg_frame_color, 
                          fg=icon_inactive_color,
                          anchor='w')
    time_label.grid(row=1, column=1, sticky='ew')
    
    # Texto do Post
    text_label = tk.Label(card_frame, 
                          text=description, 
                          font=font_roboto, 
                          bg=bg_frame_color, 
                          fg=fg_text_color,
                          wraplength=FRAME_WIDTH - 60, # Quebra de linha para caber
                          justify=tk.LEFT,
                          anchor='w')
    text_label.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 5))
    
    # Imagem do Post (Mock)
    if False:
        post_image_mock = icones.get("post_image")
        if post_image_mock:
            # Container para centralizar a imagem
            img_container = tk.Frame(card_frame, bg=bg_frame_color)
            img_container.grid(row=3, column=0, columnspan=2, pady=(5, 10))
            
            tk.Label(img_container, 
                     image=post_image_mock, 
                     bg=bg_entry_color).pack()

    # Barra de Ações (Likes, Comentários)
    actions_frame = tk.Frame(card_frame, bg=bg_frame_color)
    actions_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=(5, 0))
    
    # Função mock para botões de ação
    def mock_action(action, user):
        print(f"Ação {action} no post de {user}")

    # Botão Curtir (Mock com Emoji)
    like_btn = tk.Button(actions_frame, text="❤️ Curtir", 
                         command=lambda: mock_action("Curtir", post_data["user"]),
                         bg=bg_frame_color, fg=icon_inactive_color, bd=0, 
                         activebackground=bg_entry_color, activeforeground=purple_button_color, 
                         cursor="hand2", font=font_inter)
    like_btn.pack(side=tk.LEFT, padx=(0, 15))

    # Botão Comentar (Mock com Emoji)
    comment_btn = tk.Button(actions_frame, text="💬 Comentar", 
                            command=lambda: mock_action("Comentar", post_data["user"]),
                            bg=bg_frame_color, fg=icon_inactive_color, bd=0, 
                            activebackground=bg_entry_color, activeforeground=purple_button_color, 
                            cursor="hand2", font=font_inter)
    comment_btn.pack(side=tk.LEFT)

# ==========================================================================
# 2. View Principal (HomeView)
# ==========================================================================
def HomeView(master, switch_view_callback, icones):
    """
    Cria e exibe a tela principal do Feed.

    Args:
        master (tk.Frame): O frame pai.
        switch_view_callback (function): Função para trocar a view principal.
        icones (dict): Dicionário contendo os PhotoImages dos ícones.
    """
    # 1. Configuração do Frame Principal da View
    bg_main_color = colors.bg_main if hasattr(colors, 'bg_main') else colors["bg_main"]
    bg_frame_color = colors.bg_frame if hasattr(colors, 'bg_frame') else colors["bg_frame"]
    purple_button_color = colors.purple_button if hasattr(colors, 'purple_button') else colors["purple_button"]
    bg_entry_color = colors.bg_entry if hasattr(colors, 'bg_entry') else colors["bg_entry"]
    fg_text_color = colors.fg_text if hasattr(colors, 'fg_text') else colors["fg_text"]

    main_frame = tk.Frame(master, bg=bg_main_color, width=FRAME_WIDTH, height=FRAME_HEIGHT)
    main_frame.pack_propagate(False)
    
    # 2. Cabeçalho da View (Barra Superior Simples)
    header_frame = tk.Frame(main_frame, bg=bg_frame_color, padx=10, pady=10)
    header_frame.pack(fill='x')
    
    tk.Label(header_frame, 
             text="MIAU", 
             font=("Inter", 18, "bold"), 
             bg=bg_frame_color, 
             fg=purple_button_color).pack(pady=5)
    
    # 3. Área de Conteúdo (Rolável)
    # Cria um Canvas para permitir a rolagem
    canvas = tk.Canvas(main_frame, bg=bg_main_color, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0)
    
    # Scrollbar
    style = ttk.Style()
    style.theme_use('default')
    # Configura a Scrollbar para o tema escuro
    style.configure("Vertical.TScrollbar", background=bg_entry_color, troughcolor=bg_main_color, arrowcolor=fg_text_color)

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Frame interno onde o conteúdo será empacotado (o feed)
    content_frame = tk.Frame(canvas, bg=bg_main_color)
    
    # Cria a janela no canvas
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw", width=FRAME_WIDTH)
    
    # Função para atualizar o scroll region e o tamanho do frame interno
    def update_scroll_region(event):
        # Garante que o frame interno tenha a largura do canvas
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        # Atualiza a região de rolagem para incluir todo o conteúdo do frame interno
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    content_frame.bind("<Configure>", update_scroll_region)
    canvas.bind('<Configure>', update_scroll_region) 
    
    # Habilitar rolagem com o mouse wheel
    if sys.platform.startswith('win'): # Windows
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    elif sys.platform.startswith('linux'): # Linux
        canvas.bind_all('<Button-4>', lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all('<Button-5>', lambda e: canvas.yview_scroll(1, "units"))

    # 4. Popula o Feed com os Cards de Post
    #troca do mock, teste pelo data frame
    print(publication_df)
    for post in publication_df:
        create_post_card(content_frame, post, icones)

    # 5. Exibir a View
    return main_frame


# ==========================================================================
# TESTE (Execução Individual)
# ==========================================================================
if __name__ == "__main__":
    # Usa a função de setup do utils_icons para inicializar a janela
    test_window, root, icones = setup_test_window("Home View Teste")
    
    if test_window:
        # Frame container para simular o corpo do aplicativo
        app_body = tk.Frame(test_window, bg=colors.bg_main if hasattr(colors, 'bg_main') else colors["bg_main"])
        app_body.pack(fill="both", expand=True)

        # Função de callback de mock para a navegação
        def mock_switch_view(view_name):
            print(f"Navegação Mock: Trocando para {view_name}")

        # Cria e exibe a view de Home
        home_frame = HomeView(app_body, mock_switch_view, icones)
        home_frame.pack(fill="both", expand=True)

        # Mocka a BottomBar para garantir que o GC não colete os PhotoImages
        try:
            from utils_icons import BottomBar # Importa a barra inferior para o teste
            current_view_state = tk.StringVar(value="Home")
            
            # Cria a barra, embora não seja usada para navegação real no teste, 
            # garante que as dependências do PhotoImage sejam resolvidas.
            bottom_bar_frame = BottomBar(test_window, mock_switch_view, icones, current_view_state)
            bottom_bar_frame.pack(fill="x", side=tk.BOTTOM)
        except ImportError:
            print("BottomBar não pôde ser importada para o teste. Apenas a HomeView será exibida.")
            
        test_window.mainloop()
        # Após fechar o Toplevel, certifique-se de fechar a raiz
        try:
            root.destroy()
        except:
            pass
    else:
        print("Falha na inicialização da janela de teste. Verifique as dependências.")