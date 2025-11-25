import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from redesocial.data.userData import user_df
from redesocial.data.publicationData import publication_df
from redesocial.data.midiaData import midia_df

from redesocial.views.utils_icons import (
    colors,
    font_roboto_big,
    font_roboto,
    font_inter,
    FRAME_WIDTH,
    FRAME_HEIGHT
)

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

class HomeFeedView(tk.Frame):
    """Tela principal de Feed organizada no mesmo padrão das views Signin/Signup/Welcome"""

    def __init__(self, master, switch_view_callback=None, icones=None):
        self.switch_view_callback = switch_view_callback
        super().__init__(master, bg=DARK_THEME_COLORS["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        
        self.icones = icones or {}
        self.pack_propagate(False)

        self._create_widgets()


    # ---------------------------------------------------------------------
    # 1. Criar estrutura da tela
    # ---------------------------------------------------------------------
    def _create_widgets(self):
        # ---------- Cabeçalho ----------
        header = tk.Frame(self, bg=DARK_THEME_COLORS["bg_frame"], pady=10)
        header.pack(fill='x')

        tk.Label(header,
                 text="MIAU",
                 font=("Inter", 18, "bold"),
                 bg=DARK_THEME_COLORS["bg_frame"],
                 fg=DARK_THEME_COLORS["purple_button"]).pack()

        # ---------- Área Rolável ----------
        self.canvas = tk.Canvas(self, bg=DARK_THEME_COLORS["bg_main"], highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient='vertical',
                                  command=self.canvas.yview)

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
    def _update_scroll(self, event):
        """Mantém o scroll sempre correto."""
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # ---------------------------------------------------------------------
    # 2. Montar o Feed
    # ---------------------------------------------------------------------
    def _load_feed(self):
        """Itera o DataFrame e cria cada card."""
        for _, post in publication_df.iterrows():
            self._create_post_card(post)


    # ---------------------------------------------------------------------
    # 3. Criar o card individual
    # ---------------------------------------------------------------------
    def _create_post_card(self, post_data):
        """Cria um post no mesmo estilo da versão anterior, só que organizado."""
        card = tk.Frame(self.feed_frame, bg=DARK_THEME_COLORS["bg_frame"], padx=15, pady=15)
        card.pack(fill='x', padx=10, pady=10)

        # dados do usuário
        username = user_df[user_df["id"] == post_data["user"]]["name"].iloc[0]
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

        # ---------- Ações ----------
        actions = tk.Frame(card, bg=DARK_THEME_COLORS["bg_frame"])
        actions.pack(fill='x', pady=5)

        tk.Button(actions, text="❤️ Curtir",
                  bg=DARK_THEME_COLORS["bg_frame"],
                  fg=DARK_THEME_COLORS["icon_inactive_fg"],
                  bd=0,
                  font=font_inter).pack(side='left', padx=10)

        tk.Button(actions, text="💬 Comentar",
                  bg=DARK_THEME_COLORS["bg_frame"],
                  fg=DARK_THEME_COLORS["icon_inactive_fg"],
                  bd=0,
                  font=font_inter).pack(side='left')


    # ---------------------------------------------------------------------
    def _add_post_image(self, parent, post_data):
        """Carrega imagem se existir."""
        midias_ids = [m["id"] for m in post_data["midia_list"]]
        midias_do_post = midia_df[midia_df["id"].isin(midias_ids)]

        if len(midias_do_post) == 0:
            return

        image_path = midias_do_post.iloc[0]["original_path"]

        try:
            img = Image.open(image_path)
            img = img.resize((350, 350), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(img, master=parent)
            parent.photo = photo

            tk.Label(parent, image=photo, bg=DARK_THEME_COLORS["bg_frame"]).pack(pady=10)
        except Exception as e:
            print("Erro carregando imagem:", e)
