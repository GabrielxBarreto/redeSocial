import tkinter as tk
from tkinter import ttk
import sys

if __package__:
    from redesocial.views.utils_icons import colors, font_roboto_big, font_roboto, font_inter, FRAME_WIDTH, FRAME_HEIGHT, MOCK_RANKING_DATA, carregar_icones_mock, setup_test_window
else:
    # Fallback mínimo para teste
    class MockColors:
        bg_main = "#1e1e1e"
        bg_frame = "#252526"
        bg_entry = "#333333"
        fg_text = "#ffffff"
        purple_button = "#5653fe"
        icon_active_fg = "#5653fe"
        icon_inactive_fg = "#999999" 
    
    colors = {
        "bg_main": MockColors.bg_main,
        "bg_frame": MockColors.bg_frame,
        "bg_entry": MockColors.bg_entry,
        "fg_text": MockColors.fg_text,
        "purple_button": MockColors.purple_button,
        "icon_active_fg": MockColors.icon_active_fg,
        "icon_inactive_fg": MockColors.icon_inactive_fg,
        "accent_color": MockColors.purple_button,
        "accent_color_hover": "#4a44c0"
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


# ===============================================
# CLASSE RankingView
# ===============================================
class RankingView(tk.Frame):
    """Tela de Ranking dos Usuários"""
    def __init__(self, master, switch_view_callback, icones=None, *args, **kwargs):
        super().__init__(master, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=colors["bg_main"], *args, **kwargs)
        self.switch_view_callback = switch_view_callback
        self.icones = icones or {}
        self.pack_propagate(False)
        self._create_widgets()

    def _create_widgets(self):
        bg_main = colors["bg_main"]
        bg_frame = colors["bg_frame"]
        fg_text = colors["fg_text"]
        purple_button = colors["purple_button"]
        icon_inactive_fg = colors["icon_inactive_fg"]
        icon_active_fg = colors["icon_active_fg"]

        # =========================
        # Cabeçalho
        # =========================
        header_frame = tk.Frame(self, bg=bg_frame, padx=10, pady=10)
        header_frame.pack(fill="x")
        header_frame.columnconfigure(0, weight=0)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=0)

        # Botão voltar
        back_button = tk.Button(header_frame, text="< Voltar", font=font_roboto,
                                bg=bg_frame, fg=icon_inactive_fg, bd=0,
                                activebackground=bg_frame, activeforeground=purple_button,
                                cursor="hand2", command=self._voltar_home)
        back_button.grid(row=0, column=0, sticky="w", padx=(0, 15))

        tk.Label(header_frame, text="🏆 Ranking Global", font=font_roboto_big,
                 bg=bg_frame, fg=fg_text).grid(row=0, column=1, pady=5)

        # =========================
        # Canvas com Scroll
        # =========================
        canvas = tk.Canvas(self, bg=bg_main, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.content_frame = tk.Frame(canvas, bg=bg_main)
        self.canvas_window = canvas.create_window((0,0), window=self.content_frame, anchor="nw", width=FRAME_WIDTH)

        self.content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(self.canvas_window, width=canvas.winfo_width()))

        if sys.platform.startswith('win'):
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        elif sys.platform.startswith('linux'):
            canvas.bind_all('<Button-4>', lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all('<Button-5>', lambda e: canvas.yview_scroll(1, "units"))

        # =========================
        # Top 3 Destaques
        # =========================
        self._create_top3_cards()

        # =========================
        # Lista ranking restante
        # =========================
        self._create_ranking_list(MOCK_RANKING_DATA[3:])

    def _voltar_home(self):
        """Chama o callback para retornar à Home"""
        if self.switch_view_callback:
            self.switch_view_callback("home")

    def _create_top3_cards(self):
        bg_frame = colors["bg_frame"]
        fg_text = colors["fg_text"]
        purple_button = colors["purple_button"]
        icon_active_fg = colors["icon_active_fg"]

        top3_data = MOCK_RANKING_DATA[:3]
        podium_frame = tk.Frame(self.content_frame, bg=bg_frame, padx=20, pady=15)
        podium_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(podium_frame, text="✨ Destaques da Comunidade", font=font_roboto, bg=bg_frame, fg=fg_text).pack(pady=(0,10))
        winners_frame = tk.Frame(podium_frame, bg=bg_frame)
        winners_frame.pack()
        winners_frame.columnconfigure(0, weight=1)
        winners_frame.columnconfigure(1, weight=1)
        winners_frame.columnconfigure(2, weight=1)

        def create_card(parent, user_data, col, rank_text, is_top=False):
            card_bg = colors["bg_entry"] if is_top else colors["bg_main"]
            card = tk.Frame(parent, bg=card_bg, padx=10, pady=10, relief=tk.FLAT, bd=0)
            card.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
            tk.Label(card, text=rank_text, font=("Roboto",14,"bold"), bg=card_bg, fg=colors["purple_button"]).pack()
            profile_pic_mock = self.icones.get("profile_pic")
            if profile_pic_mock:
                tk.Label(card, image=profile_pic_mock, bg=card_bg).pack(pady=5)
            tk.Label(card, text=user_data["username"], font=font_roboto, bg=card_bg, fg=colors["fg_text"]).pack()
            tk.Label(card, text=f'{user_data["points"]} Pontos', font=font_inter, bg=card_bg, fg=icon_active_fg).pack()

        # 1º
        create_card(winners_frame, top3_data[0], 1, "🥇 1º", is_top=True)
        # 2º
        create_card(winners_frame, top3_data[1], 0, "🥈 2º")
        # 3º
        create_card(winners_frame, top3_data[2], 2, "🥉 3º")

    def _create_ranking_list(self, data):
        bg_frame = colors["bg_frame"]
        bg_main = colors["bg_main"]
        fg_text = colors["fg_text"]
        purple_button = colors["purple_button"]

        tk.Label(self.content_frame, text="Outros Contribuintes", font=font_roboto_big, bg=bg_main, fg=fg_text).pack(anchor='w', padx=10, pady=(10,5))

        for user_data in data:
            is_current = user_data["username"] == "papai.dev"
            row_bg = bg_frame if not is_current else purple_button
            row_fg = fg_text if not is_current else bg_main
            row_frame = tk.Frame(self.content_frame, bg=row_bg, padx=15, pady=8)
            row_frame.pack(fill='x', padx=10, pady=2)
            row_frame.columnconfigure(0, minsize=40)
            row_frame.columnconfigure(1, weight=1)
            row_frame.columnconfigure(2, minsize=80)
            tk.Label(row_frame, text=f'{user_data["rank"]}º', font=font_roboto_big, bg=row_bg, fg=row_fg).grid(row=0, column=0, sticky='w')
            tk.Label(row_frame, text=user_data["username"], font=font_roboto, bg=row_bg, fg=row_fg, anchor='w').grid(row=0, column=1, sticky='w', padx=(10,0))
            tk.Label(row_frame, text=f'{user_data["points"]} Pts', font=("Roboto",12,"bold"), bg=row_bg, fg=row_fg).grid(row=0, column=2, sticky='e')


# ===============================================
# TESTE INDIVIDUAL
# ===============================================
if __name__ == "__main__":
    test_window, root, icones = setup_test_window("Ranking View Teste")
    if test_window:
        app_body = tk.Frame(test_window, bg=colors["bg_main"])
        app_body.pack(fill="both", expand=True)

        def mock_switch(view_name):
            print(f"DEBUG: Trocando para {view_name}")
            test_window.destroy()  # fecha a janela mock

        ranking_view = RankingView(app_body, mock_switch, icones)
        ranking_view.pack(fill="both", expand=True)
        test_window.mainloop()
        try:
            root.destroy()
        except:
            pass
