import tkinter as tk
from tkinter import ttk
import sys
import os

# Importa as utilidades do arquivo pai (utils_icons.py)
# NOTA: Assumimos que utils_icons.py está no mesmo diretório ou em um caminho de módulo acessível
try:
    from utils_icons import (
        colors, 
        font_roboto_big, 
        font_roboto, 
        font_inter, 
        FRAME_WIDTH, 
        FRAME_HEIGHT, 
        MOCK_RANKING_DATA, 
        carregar_icones_mock, 
        setup_test_window
    )
except ImportError:
    # Fallback para execução local ou ambiente de teste
    print("Erro ao importar utilidades. Verifique se 'utils_icons.py' está no caminho correto.")
    # No ambiente Canvas, estas variáveis devem ser resolvidas pelo módulo principal.
    
    # Mocks MÍNIMOS para evitar quebras no teste unitário
    class MockColors:
        bg_main = "#1e1e1e"
        bg_frame = "#252526"
        bg_entry = "#333333"
        fg_text = "#ffffff"
        purple_button = "#5653fe"
        icon_active_fg = "#5653fe"
    colors = MockColors()
    font_roboto_big = ("Roboto", 16, "bold")
    font_roboto = ("Roboto", 12)
    font_inter = ("Inter", 10)
    FRAME_WIDTH = 420
    FRAME_HEIGHT = 720
    MOCK_RANKING_DATA = [
        {"rank": 1, "username": "AliceDev", "points": 1250, "projects": 5},
        {"rank": 2, "username": "BobCoder", "points": 980, "projects": 3},
        {"rank": 3, "username": "papai.dev", "points": 850, "projects": 4},
        {"rank": 4, "username": "CarolTech", "points": 720, "projects": 2},
    ]
    def setup_test_window(*args): return None, None, {}
    def carregar_icones_mock(): return {}


def RankingView(master, switch_view_callback, icones):
    """
    Cria e exibe a tela de Ranking dos usuários.

    Args:
        master (tk.Frame): O frame pai onde esta view será empacotada.
        switch_view_callback (function): Função para trocar a view principal.
        icones (dict): Dicionário contendo os PhotoImages dos ícones.
    """
    # 1. Configuração do Frame Principal da View
    main_frame = tk.Frame(master, bg=colors["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
    main_frame.pack_propagate(False) # Impedir que o frame se redimensione automaticamente
    
    # 2. Cabeçalho da View
    header_frame = tk.Frame(main_frame, bg=colors["bg_frame"], padx=10, pady=10)
    header_frame.pack(fill='x')
    
    tk.Label(header_frame, 
             text="🏆 Ranking Global", 
             font=font_roboto_big, 
             bg=colors["bg_frame"], 
             fg=colors["fg_text"]).pack(pady=5)
    
    # 3. Área de Conteúdo (Rolável)
    # Cria um Canvas para permitir a rolagem
    canvas = tk.Canvas(main_frame, bg=colors["bg_main"], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0)
    
    # Cria a Scrollbar e a associa ao Canvas
    # Configuração de estilo escuro para a Scrollbar
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Vertical.TScrollbar", background=colors["bg_entry"], troughcolor=colors["bg_main"], arrowcolor=colors["fg_text"])

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Frame interno onde o conteúdo será empacotado
    content_frame = tk.Frame(canvas, bg=colors["bg_main"])
    
    # Cria a janela no canvas
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw", width=FRAME_WIDTH)
    
    # Função para atualizar o scroll region e o tamanho do frame interno
    def update_scroll_region(event):
        # Garante que o frame interno tenha a largura do canvas
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        # Atualiza a região de rolagem para incluir todo o conteúdo do frame interno
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    content_frame.bind("<Configure>", update_scroll_region)
    canvas.bind('<Configure>', update_scroll_region) # Para reconfigurar o scroll ao redimensionar (se fosse permitido)
    
    # Habilitar rolagem com o mouse wheel
    if sys.platform.startswith('win'): # Windows
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    elif sys.platform.startswith('linux'): # Linux
        canvas.bind_all('<Button-4>', lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all('<Button-5>', lambda e: canvas.yview_scroll(1, "units"))
    # MacOS usa o evento padrão do Tkinter, que é <MouseWheel> mas geralmente funciona com a configuração Windows ou Linux.


    # ==========================================================================
    # 4. Cartão TOP 3 (Destaque)
    # ==========================================================================
    
    top3_data = MOCK_RANKING_DATA[:3]

    # Frame para conter o pódio
    podium_frame = tk.Frame(content_frame, bg=colors["bg_frame"], padx=20, pady=15)
    podium_frame.pack(fill='x', padx=10, pady=10)
    
    # Título do Pódio
    tk.Label(podium_frame, text="✨ Destaques da Comunidade", font=font_roboto, bg=colors["bg_frame"], fg=colors["fg_text"]).pack(pady=(0, 10))

    # Frame para 2º, 1º e 3º colocados (usando grid para layout)
    winners_frame = tk.Frame(podium_frame, bg=colors["bg_frame"])
    winners_frame.pack()
    
    # Configurações do Grid
    winners_frame.columnconfigure(0, weight=1) # 2º lugar
    winners_frame.columnconfigure(1, weight=1) # 1º lugar
    winners_frame.columnconfigure(2, weight=1) # 3º lugar

    # Estilo dos Cards do Pódio
    def create_podium_card(parent, user_data, col, rank_text, is_top=False):
        
        # Cor de fundo mais clara para destacar o topo
        card_bg = colors["bg_entry"] if is_top else colors["bg_main"]
        card_fg = colors["fg_text"]
        
        card = tk.Frame(parent, bg=card_bg, padx=10, pady=10, relief=tk.FLAT, bd=0)
        card.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        # Rank Text
        rank_label = tk.Label(card, text=rank_text, font=("Roboto", 14, "bold"), bg=card_bg, fg=colors["purple_button"])
        rank_label.pack()
        
        # Ícone de Perfil (Mock: um quadrado colorido)
        # Usamos o mock de profile_pic
        profile_pic_mock = icones.get("profile_pic")
        if profile_pic_mock:
            tk.Label(card, image=profile_pic_mock, bg=card_bg).pack(pady=5)
            
        # Nome de Usuário
        tk.Label(card, text=user_data["username"], font=font_roboto, bg=card_bg, fg=card_fg).pack()
        
        # Pontos
        tk.Label(card, text=f'{user_data["points"]} Pontos', font=font_inter, bg=card_bg, fg=colors["icon_active_fg"]).pack()

    # 1º Lugar (Coluna do Meio)
    create_podium_card(winners_frame, top3_data[0], 1, "🥇 1º", is_top=True)
    
    # 2º Lugar (Coluna Esquerda)
    create_podium_card(winners_frame, top3_data[1], 0, "🥈 2º")
    
    # 3º Lugar (Coluna Direita)
    create_podium_card(winners_frame, top3_data[2], 2, "🥉 3º")

    # ==========================================================================
    # 5. Lista de Ranking (4º em diante)
    # ==========================================================================
    
    list_title_frame = tk.Frame(content_frame, bg=colors["bg_main"], padx=10)
    list_title_frame.pack(fill='x', pady=(10, 5))
    tk.Label(list_title_frame, text="Outros Contribuintes", font=font_roboto_big, bg=colors["bg_main"], fg=colors["fg_text"]).pack(anchor='w')

    
    def create_ranking_row(parent, user_data, current_username="papai.dev"):
        # Se o usuário atual estiver logado (mockado como "papai.dev"), destaque a linha.
        is_current_user = (user_data["username"] == current_username)
        row_bg = colors["bg_frame"] if not is_current_user else colors["purple_button"]
        row_fg = colors["fg_text"] if not is_current_user else colors["bg_frame"]
        
        row_frame = tk.Frame(parent, bg=row_bg, padx=15, pady=8)
        row_frame.pack(fill='x', padx=10, pady=2)
        
        # Configurar Grid para a linha
        row_frame.columnconfigure(0, minsize=40) # Rank
        row_frame.columnconfigure(1, weight=1)  # Nome
        row_frame.columnconfigure(2, minsize=80) # Pontos
        
        # Rank
        rank_label = tk.Label(row_frame, text=f'{user_data["rank"]}º', font=font_roboto_big, bg=row_bg, fg=row_fg)
        rank_label.grid(row=0, column=0, sticky='w')
        
        # Nome de Usuário
        name_label = tk.Label(row_frame, text=user_data["username"], font=font_roboto, bg=row_bg, fg=row_fg, anchor='w')
        name_label.grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        # Pontos
        points_label = tk.Label(row_frame, text=f'{user_data["points"]} Pts', font=("Roboto", 12, "bold"), bg=row_bg, fg=row_fg)
        points_label.grid(row=0, column=2, sticky='e')

    # Itera sobre os dados a partir do 4º colocado (MOCK_RANKING_DATA[3:])
    for user in MOCK_RANKING_DATA[3:]:
        create_ranking_row(content_frame, user)


    # ==========================================================================
    # 6. Exibir a View
    # ==========================================================================
    return main_frame


# ==========================================================================
# TESTE (Execução Individual)
# ==========================================================================
if __name__ == "__main__":
    # Usa a função de setup do utils_icons para inicializar a janela
    # Nota: Se o utils_icons.py não estiver disponível, o fallback será usado.
    test_window, root, icones = setup_test_window("Ranking View Teste")
    
    if test_window:
        # Frame container para simular o corpo do aplicativo
        app_body = tk.Frame(test_window, bg=colors["bg_main"])
        app_body.pack(fill="both", expand=True)

        # Função de callback de mock para a navegação
        def mock_switch_view(view_name):
            print(f"Navegação Mock: Trocando para {view_name}")

        # Cria e exibe a view de Ranking
        ranking_frame = RankingView(app_body, mock_switch_view, icones)
        ranking_frame.pack(fill="both", expand=True)

        test_window.mainloop()
        # Após fechar o Toplevel, certifique-se de fechar a raiz
        try:
            root.destroy()
        except:
            pass
    else:
        print("Falha na inicialização da janela de teste. Verifique as dependências.")