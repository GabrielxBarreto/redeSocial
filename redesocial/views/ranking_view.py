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
    
    # Mocks MÍNIMOS para evitar quebras no teste unitário
    class MockColors:
        bg_main = "#1e1e1e"
        bg_frame = "#252526"
        bg_entry = "#333333"
        fg_text = "#ffffff"
        purple_button = "#5653fe"
        icon_active_fg = "#5653fe"
        icon_inactive_fg = "#999999" 
    
    # No Fallback, colors É A CLASSE, então simulamos um dicionário para manter a compatibilidade da view.
    colors = {
        "bg_main": MockColors.bg_main,
        "bg_frame": MockColors.bg_frame,
        "bg_entry": MockColors.bg_entry,
        "fg_text": MockColors.fg_text,
        "purple_button": MockColors.purple_button,
        "icon_active_fg": MockColors.icon_active_fg,
        "icon_inactive_fg": MockColors.icon_inactive_fg
    }
    
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
    def setup_test_window(*args): 
        root = tk.Tk()
        root.withdraw()
        window = tk.Toplevel(root)
        window.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}")
        return window, root, {}
    def carregar_icones_mock(): 
        MOCK_ICON = tk.PhotoImage(width=30, height=30)
        return {"profile_pic": MOCK_ICON} 


def RankingView(master, switch_view_callback, icones):
    """
    Cria e exibe a tela de Ranking dos usuários.
    
    Args:
        master (tk.Frame): O frame pai onde esta view será empacotada.
        switch_view_callback (function): Função para trocar a view principal.
        icones (dict): Dicionário contendo os PhotoImages dos ícones.
    """
    # 1. Configuração do Frame Principal da View
    # CORREÇÃO: Acessando as cores usando colchetes (dicionário)
    bg_main = colors["bg_main"]
    bg_frame = colors["bg_frame"]
    fg_text = colors["fg_text"]
    purple_button = colors["purple_button"]
    bg_entry = colors["bg_entry"]
    icon_inactive_fg = colors["icon_inactive_fg"] 
    icon_active_fg = colors["icon_active_fg"]
    
    main_frame = tk.Frame(master, bg=bg_main, width=FRAME_WIDTH, height=FRAME_HEIGHT)
    main_frame.pack_propagate(False) 
    
    # 2. Cabeçalho da View (Organizado com GRID)
    header_frame = tk.Frame(main_frame, bg=bg_frame, padx=10, pady=10)
    header_frame.pack(fill='x')
    
    header_frame.columnconfigure(0, weight=0) # Botão voltar (fixo)
    header_frame.columnconfigure(1, weight=1) # Título (expansível)
    header_frame.columnconfigure(2, weight=0) # Espaço / Botão de ação (opcional)

    # --- Botão Voltar (Home) ---
    def go_back():
        # O botão "Voltar" tipicamente leva de volta para a Home
        switch_view_callback("Home") 
    
    back_button = tk.Button(header_frame, 
                            text="< Voltar", # Simula um ícone de seta
                            command=go_back,
                            font=font_roboto,
                            bg=bg_frame,
                            fg=icon_inactive_fg,
                            bd=0, 
                            activebackground=bg_frame,
                            activeforeground=purple_button,
                            cursor="hand2")
    back_button.grid(row=0, column=0, sticky='w', padx=(0, 15))
    
    # --- Título da View ---
    tk.Label(header_frame, 
             text="🏆 Ranking Global", 
             font=font_roboto_big, 
             bg=bg_frame, 
             fg=fg_text).grid(row=0, column=1, pady=5)
    
    # 3. Área de Conteúdo (Rolável)
    canvas = tk.Canvas(main_frame, bg=bg_main, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0)
    
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Vertical.TScrollbar", background=bg_entry, troughcolor=bg_main, arrowcolor=fg_text)

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    content_frame = tk.Frame(canvas, bg=bg_main)
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw", width=FRAME_WIDTH)
    
    def update_scroll_region(event):
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    content_frame.bind("<Configure>", update_scroll_region)
    canvas.bind('<Configure>', update_scroll_region) 
    
    if sys.platform.startswith('win'): 
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    elif sys.platform.startswith('linux'): 
        canvas.bind_all('<Button-4>', lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all('<Button-5>', lambda e: canvas.yview_scroll(1, "units"))


    # ==========================================================================
    # 4. Cartão TOP 3 (Destaque)
    # ==========================================================================
    
    top3_data = MOCK_RANKING_DATA[:3]

    podium_frame = tk.Frame(content_frame, bg=bg_frame, padx=20, pady=15)
    podium_frame.pack(fill='x', padx=10, pady=10)
    
    tk.Label(podium_frame, text="✨ Destaques da Comunidade", font=font_roboto, bg=bg_frame, fg=fg_text).pack(pady=(0, 10))

    winners_frame = tk.Frame(podium_frame, bg=bg_frame)
    winners_frame.pack()
    
    winners_frame.columnconfigure(0, weight=1) 
    winners_frame.columnconfigure(1, weight=1) 
    winners_frame.columnconfigure(2, weight=1) 

    def create_podium_card(parent, user_data, col, rank_text, is_top=False):
        
        card_bg = bg_entry if is_top else bg_main
        card_fg = fg_text
        
        card = tk.Frame(parent, bg=card_bg, padx=10, pady=10, relief=tk.FLAT, bd=0)
        card.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        rank_label = tk.Label(card, text=rank_text, font=("Roboto", 14, "bold"), bg=card_bg, fg=purple_button)
        rank_label.pack()
        
        # Ícone de Perfil (Mock)
        profile_pic_mock = icones.get("profile_pic")
        if profile_pic_mock:
            tk.Label(card, image=profile_pic_mock, bg=card_bg).pack(pady=5)
            
        tk.Label(card, text=user_data["username"], font=font_roboto, bg=card_bg, fg=card_fg).pack()
        
        tk.Label(card, text=f'{user_data["points"]} Pontos', font=font_inter, bg=card_bg, fg=icon_active_fg).pack()

    # 1º Lugar (Coluna do Meio)
    create_podium_card(winners_frame, top3_data[0], 1, "🥇 1º", is_top=True)
    
    # 2º Lugar (Coluna Esquerda)
    create_podium_card(winners_frame, top3_data[1], 0, "🥈 2º")
    
    # 3º Lugar (Coluna Direita)
    create_podium_card(winners_frame, top3_data[2], 2, "🥉 3º")

    # ==========================================================================
    # 5. Lista de Ranking (4º em diante)
    # ==========================================================================
    
    list_title_frame = tk.Frame(content_frame, bg=bg_main, padx=10)
    list_title_frame.pack(fill='x', pady=(10, 5))
    tk.Label(list_title_frame, text="Outros Contribuintes", font=font_roboto_big, bg=bg_main, fg=fg_text).pack(anchor='w')

    
    def create_ranking_row(parent, user_data, current_username="papai.dev"):
        is_current_user = (user_data["username"] == current_username)
        row_bg = bg_frame if not is_current_user else purple_button
        row_fg = fg_text if not is_current_user else bg_frame
        
        row_frame = tk.Frame(parent, bg=row_bg, padx=15, pady=8)
        row_frame.pack(fill='x', padx=10, pady=2)
        
        row_frame.columnconfigure(0, minsize=40) 
        row_frame.columnconfigure(1, weight=1)  
        row_frame.columnconfigure(2, minsize=80) 
        
        rank_label = tk.Label(row_frame, text=f'{user_data["rank"]}º', font=font_roboto_big, bg=row_bg, fg=row_fg)
        rank_label.grid(row=0, column=0, sticky='w')
        
        name_label = tk.Label(row_frame, text=user_data["username"], font=font_roboto, bg=row_bg, fg=row_fg, anchor='w')
        name_label.grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        points_label = tk.Label(row_frame, text=f'{user_data["points"]} Pts', font=("Roboto", 12, "bold"), bg=row_bg, fg=row_fg)
        points_label.grid(row=0, column=2, sticky='e')

    for user in MOCK_RANKING_DATA[3:]:
        create_ranking_row(content_frame, user)


    # 6. Exibir a View
    return main_frame


# ==========================================================================
# TESTE (Execução Individual)
# ==========================================================================
if __name__ == "__main__":
    test_window, root, icones = setup_test_window("Ranking View Teste")
    
    if test_window:
        # CORREÇÃO: Acessando a cor no bloco de teste com colchetes
        app_body = tk.Frame(test_window, bg=colors["bg_main"])
        app_body.pack(fill="both", expand=True)

        def mock_switch_view(view_name):
            print(f"Navegação Mock: Trocando para {view_name}. Fechando janela de teste.")
            test_window.destroy() # Fechar a janela ao "voltar" no mock

        ranking_frame = RankingView(app_body, mock_switch_view, icones)
        ranking_frame.pack(fill="both", expand=True)

        test_window.mainloop()
        
        try:
            root.destroy()
        except:
            pass
    else:
        print("Falha na inicialização da janela de teste. Verifique as dependências.")