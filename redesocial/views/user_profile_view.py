import tkinter as tk
from tkinter import scrolledtext, messagebox

# Importação direta (sem ponto) para funcionar como script autônomo
from utils_icons import (
    colors, font_roboto_big, font_inter, font_inter_small, 
    MOCK_PROFILE_DATA, icones_mock, 
    load_user_profile_data, update_user_bio, update_user_interests,
    setup_test_window
)

class UserProfileView:
    """
    Representa a tela de perfil do usuário, com dados mockados,
    bio editável e feed de posts.
    """
    def __init__(self, master_frame, icones):
        self.master_frame = master_frame
        self.icones = icones
        self.user_data = load_user_profile_data("current_user")
        
        # Frame principal com scroll (simulado)
        self.main_frame = tk.Frame(master_frame, bg=colors["bg_frame"])
        self.main_frame.pack(fill="both", expand=True)

        # Usamos Canvas e Frame interno para permitir a rolagem
        self.canvas = tk.Canvas(self.main_frame, bg=colors["bg_frame"], highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        self.scrollable_frame = tk.Frame(self.canvas, bg=colors["bg_frame"])
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=420)
        
        # O frame interno é onde todo o conteúdo do perfil será adicionado
        self._build_ui()
        
        # Permite que o scrollable_frame se ajuste ao redimensionamento do canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Adicionar eventos de rolagem do mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Armazena referências de imagem para evitar Garbage Collection
        self.image_refs = [
            self.icones.get("cover_image"), 
            self.icones.get("profile_pic"),
            self.icones.get("location_icon"),
            self.icones.get("education_icon"),
            self.icones.get("friends_icon")
        ]
        
    def _on_mousewheel(self, event):
        """Função para tratar a rolagem do mouse no Canvas."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def _build_ui(self):
        """Constrói todos os componentes visuais da tela de perfil."""
        
        # --- 1. CABEÇALHO (CAPA E FOTO) ---
        header_frame = tk.Frame(self.scrollable_frame, bg=colors["bg_frame"])
        header_frame.pack(fill="x")
        
        # Imagem de Capa (Placeholder)
        cover_label = tk.Label(header_frame, image=self.icones.get("cover_image"), bg=colors["bg_frame"])
        cover_label.pack(fill="x")

        # Frame da Foto de Perfil e Nome
        profile_info_frame = tk.Frame(header_frame, bg=colors["bg_frame"])
        profile_info_frame.pack(fill="x", pady=(0, 10))
        
        # Foto de Perfil (Placeholder)
        profile_pic_label = tk.Label(profile_info_frame, image=self.icones.get("profile_pic"), bg=colors["bg_frame"])
        # Posiciona a foto sobrepondo a borda inferior da capa
        profile_pic_label.place(x=20, y=-50) 
        
        # Nome do Usuário
        tk.Label(profile_info_frame, text=self.user_data["username"], 
                 font=font_roboto_big, bg=colors["bg_frame"], fg=colors["fg_text"],
                 anchor="w").pack(padx=(120, 10), pady=(10, 0), fill="x")
        
        # Botão de Amigos (Mock)
        friends_button = tk.Button(profile_info_frame, text=" 54 Amigos", 
                                   image=self.icones.get("friends_icon"), compound="left",
                                   bg=colors["bg_button"], fg=colors["fg_text"], 
                                   activebackground=colors["active_bg_button"], relief="flat", 
                                   font=font_inter_small, padx=5, pady=2)
        friends_button.pack(padx=(120, 10), fill="x")

        # --- 2. BIOGRAFIA E INFORMAÇÕES BÁSICAS ---
        info_frame = tk.Frame(self.scrollable_frame, bg=colors["bg_frame"])
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # Descrição/Bio (Atualizável)
        self.bio_label = tk.Label(info_frame, text=self.user_data["bio"], 
                                  bg=colors["bg_frame"], fg=colors["fg_entry"], 
                                  font=font_inter, wraplength=380, justify="left", anchor="w")
        self.bio_label.pack(fill="x", pady=(0, 10))
        
        # Botão Editar Bio
        btn_edit_bio = tk.Button(info_frame, text="Editar Bio", command=self._open_bio_editor,
                                 bg=colors["purple_button"], fg=colors["fg_text"], 
                                 activebackground=colors["active_bg_button"], relief="flat", 
                                 font=font_inter_small)
        btn_edit_bio.pack(side="right", anchor="e")

        # Informações Detalhadas (Localização, Educação)
        self._create_info_line(info_frame, self.icones.get("location_icon"), self.user_data["location"])
        self._create_info_line(info_frame, self.icones.get("education_icon"), self.user_data["education"])
        
        # --- 3. INTERESSES ---
        interests_frame = tk.Frame(self.scrollable_frame, bg=colors["bg_frame"])
        interests_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(interests_frame, text="Interesses:", font=font_roboto, bg=colors["bg_frame"], fg=colors["fg_text"], anchor="w").pack(fill="x")
        
        self.interests_var = tk.StringVar(value=", ".join(self.user_data["interests"]))
        self.interests_label = tk.Label(interests_frame, textvariable=self.interests_var, 
                                        bg=colors["bg_frame"], fg=colors["fg_entry"], 
                                        font=font_inter, wraplength=380, justify="left", anchor="w")
        self.interests_label.pack(fill="x", pady=(0, 10))
        
        btn_edit_interests = tk.Button(interests_frame, text="Editar Interesses", command=self._open_interests_editor,
                                       bg=colors["bg_button"], fg=colors["fg_text"], 
                                       activebackground=colors["active_bg_button"], relief="flat", 
                                       font=font_inter_small)
        btn_edit_interests.pack(side="right", anchor="e", pady=(0, 5))


        # --- 4. SEPARADOR E FEED DE POSTS ---
        tk.Frame(self.scrollable_frame, height=2, bg=colors["bg_button"]).pack(fill="x", padx=20, pady=15)
        
        tk.Label(self.scrollable_frame, text="Minhas Publicações", font=font_roboto_big, bg=colors["bg_frame"], fg=colors["fg_text"]).pack(pady=(0, 10))
        
        # Feed de Posts do Usuário (Simulado)
        for post in self.user_data["posts"]:
            self._create_post_card(self.scrollable_frame, self.user_data["username"], post)

    def _create_info_line(self, parent, icon, text):
        """Cria uma linha com ícone e texto para informações como localização/educação."""
        line_frame = tk.Frame(parent, bg=colors["bg_frame"])
        line_frame.pack(fill="x", pady=2)
        
        icon_label = tk.Label(line_frame, image=icon, bg=colors["bg_frame"])
        icon_label.pack(side="left")
        
        tk.Label(line_frame, text=text, bg=colors["bg_frame"], fg=colors["fg_text"], font=font_inter, anchor="w").pack(side="left", padx=5)

    def _create_post_card(self, parent, username, post):
        """Cria um card visual para um post individual."""
        card = tk.Frame(parent, bg=colors["bg_entry"], padx=15, pady=10, relief="raised", bd=1)
        card.pack(fill="x", padx=20, pady=5)
        
        # Header do Post
        header = tk.Frame(card, bg=colors["bg_entry"])
        header.pack(fill="x", pady=(0, 5))
        tk.Label(header, text=username, font=font_roboto_big, fg=colors["purple_button"], bg=colors["bg_entry"]).pack(side="left")
        
        # Conteúdo do Post
        tk.Label(card, text=post["text"], font=font_inter, fg=colors["fg_text"], bg=colors["bg_entry"], 
                 wraplength=350, justify="left").pack(fill="x")
        
        # Imagem (se houver)
        if post["has_image"] and self.icones.get("post_image"):
            # O post_image é um ícone de mock estático
            img_label = tk.Label(card, image=self.icones["post_image"], bg=colors["bg_entry"])
            img_label.pack(pady=10)
            # Armazena referência da imagem do post
            card.image_ref = self.icones["post_image"] 

    # --- FUNÇÕES DE EDIÇÃO ---

    def _open_bio_editor(self):
        """Abre uma nova janela (Toplevel) para editar a Bio."""
        editor = tk.Toplevel(self.master_frame)
        editor.title("Editar Biografia")
        editor.geometry("350x250")
        editor.config(bg=colors["bg_main"])
        
        tk.Label(editor, text="Nova Biografia:", bg=colors["bg_main"], fg=colors["fg_text"], font=font_inter).pack(pady=10)
        
        bio_text = scrolledtext.ScrolledText(editor, height=5, width=40, font=font_inter,
                                             bg=colors["bg_entry"], fg=colors["fg_entry"], 
                                             insertbackground=colors["fg_entry"], wrap="word")
        bio_text.insert("1.0", self.user_data["bio"])
        bio_text.pack(padx=10, pady=5)
        
        def save():
            nova_bio = bio_text.get("1.0", tk.END).strip()
            update_user_bio(self.user_data["username"], nova_bio)
            self.user_data["bio"] = nova_bio # Atualiza o dado localmente
            self.bio_label.config(text=nova_bio) # Atualiza a label na tela principal
            editor.destroy()

        tk.Button(editor, text="Salvar Bio", command=save,
                  bg=colors["purple_button"], fg=colors["fg_text"], 
                  activebackground=colors["active_bg_button"], relief="flat", 
                  font=font_inter).pack(pady=10)
                  
    def _open_interests_editor(self):
        """Abre uma nova janela (Toplevel) para editar Interesses."""
        editor = tk.Toplevel(self.master_frame)
        editor.title("Editar Interesses")
        editor.geometry("350x200")
        editor.config(bg=colors["bg_main"])
        
        tk.Label(editor, text="Interesses (separados por vírgula):", bg=colors["bg_main"], fg=colors["fg_text"], font=font_inter).pack(pady=10)
        
        # Converte a lista de interesses em uma string separada por vírgulas para edição
        initial_text = ", ".join(self.user_data["interests"])
        interests_entry = tk.Entry(editor, width=40, font=font_inter,
                                   bg=colors["bg_entry"], fg=colors["fg_entry"], 
                                   insertbackground=colors["fg_entry"])
        interests_entry.insert(0, initial_text)
        interests_entry.pack(padx=10, pady=5)
        
        def save():
            interesses_string = interests_entry.get().strip()
            # Converte a string de volta para lista
            novos_interesses = [i.strip() for i in interesses_string.split(',') if i.strip()]
            
            update_user_interests(self.user_data["username"], novos_interesses)
            self.user_data["interests"] = novos_interesses # Atualiza o dado localmente
            self.interests_var.set(", ".join(novos_interesses)) # Atualiza a label
            editor.destroy()

        tk.Button(editor, text="Salvar Interesses", command=save,
                  bg=colors["purple_button"], fg=colors["fg_text"], 
                  activebackground=colors["active_bg_button"], relief="flat", 
                  font=font_inter).pack(pady=10)


def criar_aba_perfil(container_frame, icones):
    """Função wrapper para criar a tela de perfil."""
    # Instancia a classe UserProfileView, que gerencia seu próprio layout e scroll.
    profile_view = UserProfileView(container_frame, icones)
    return profile_view.main_frame

# --- BLOCO DE TESTE INDIVIDUAL ---
if __name__ == "__main__":
    test_window, root = setup_test_window("Teste Individual: Perfil do Usuário")
    
    frame = criar_aba_perfil(test_window, icones_mock)
    frame.pack(fill="both", expand=True)
    
    root.mainloop()