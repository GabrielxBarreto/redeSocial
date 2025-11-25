import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk, ImageDraw
import sys

# --- Configurações e Cores ---
BG_MAIN = "#1A1A1A"
ACCENT_COLOR = "#6F42C1"
TEXT_COLOR = "#FFFFFF"
SUBTEXT_COLOR = "#A0A0A0"
ENTRY_BG = "#333333" # Cor para os campos de entrada
SUCCESS_COLOR = "#4CAF50" # Cor para mensagens de sucesso

# Largura para simulação mobile
MOBILE_WIDTH = 400
# Altura para simulação mobile
MOBILE_HEIGHT = 700

class UserProfileView(tk.Frame):
    def __init__(self, master, user_data, navigate_back_callback):
        super().__init__(master, bg=BG_MAIN)
        self.master = master
        # Garantir que tenhamos um username para exibir
        if 'username' not in user_data:
             user_data['username'] = 'stefan_h' 
        
        self.user_data = user_data.copy() 
        self.navigate_back_callback = navigate_back_callback

        # Variáveis de estado
        self.is_editing = False
        self.banner_id = None 

        # Variáveis de texto editáveis (Entry/Text)
        initial_interests = ", ".join(self.user_data.get('interests', ["Design", "Marketing", "Fotografia"]))
        self.interests_var = tk.StringVar(value=initial_interests)
        self.description_var = tk.StringVar(value=self.user_data.get('description', 'Arte é minha maior paixão...'))


        #  CAMINHO DAS IMAGENS
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(script_dir, 'img')

        self.images = {}

        self._load_images()
        self._create_widgets()

    def _get_image_path(self, filename):
        """Retorna o caminho absoluto para um arquivo de imagem."""
        return os.path.join(self.img_dir, filename)

    def _load_images(self):
        """Carrega e armazena todas as imagens necessárias com tratamento de erro"""
        image_files = {
            'cover': 'cover_image.png',
            'profile': 'profile_pic.png',
            'follow': 'friend_icon.png',
            'location': 'location_icon.png',
            'education': 'education_icon.png',
            'back': 'back_arrow.png',
        }

        for name, filename in image_files.items():
            path = self._get_image_path(filename)
            try:
                pil_img = Image.open(path)

                if name == 'cover':
                    pil_img = pil_img.resize((MOBILE_WIDTH, 120), Image.Resampling.LANCZOS)
                elif name == 'profile':
                    size = 100
                    pil_img = pil_img.resize((size, size), Image.Resampling.LANCZOS)
                    mask = Image.new('L', (size, size), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, size, size), fill=255)
                    pil_img.putalpha(mask)
                elif name == 'back':
                    # Aumentando o ícone de voltar para (30x30)
                    pil_img = pil_img.resize((30, 30), Image.Resampling.LANCZOS)
                elif name in ['follow', 'location', 'education']:
                    pil_img = pil_img.resize((22, 22), Image.Resampling.LANCZOS)

                self.images[name] = ImageTk.PhotoImage(pil_img)
            except FileNotFoundError:
                print(f"ERRO: Arquivo de imagem não encontrado: {filename}. Usando fallback.")
                self.images[name] = None
            except Exception as e:
                print(f"ERRO ao carregar {filename}: {e}")
                self.images[name] = None

    def _create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        
        # --- Frame para o Banner de Notificação (posicionado no topo) ---
        self.banner_frame = tk.Frame(self, bg=SUCCESS_COLOR, height=30)
        self.banner_label = tk.Label(self.banner_frame, text="", bg=SUCCESS_COLOR, fg=TEXT_COLOR, font=("Arial", 10))
        self.banner_label.pack(expand=True, fill="both")
        # Inicialmente não gridado

        # --- Imagem de Capa e Botão Voltar ---
        cover_frame = tk.Frame(self, bg=BG_MAIN)
        cover_frame.grid(row=0, column=0, sticky="ew")

        cover_label = tk.Label(cover_frame, image=self.images.get('cover'), width=MOBILE_WIDTH)
        if self.images.get('cover'):
            cover_label.image = self.images.get('cover')
        else:
            cover_label.config(text="Capa", bg="#333333", fg=SUBTEXT_COLOR, height=8)
        cover_label.pack(fill="x", anchor="n")

        # Botão Voltar
        back_button = tk.Button(cover_frame, image=self.images.get('back'), command=self._on_back_click,
                                bg=BG_MAIN, activebackground=BG_MAIN, relief="flat", bd=0, padx=10, pady=10)
        if self.images.get('back'):
            back_button.image = self.images.get('back')
        else:
            back_button.config(text="<")
        back_button.place(x=0, y=0) 

        # --- Informações e Ações ---
        self.info_frame = tk.Frame(self, bg=BG_MAIN, padx=15, pady=5)
        self.info_frame.grid(row=1, column=0, sticky="ew")
        self.info_frame.grid_columnconfigure(0, weight=1)

        header_row = tk.Frame(self.info_frame, bg=BG_MAIN)
        header_row.pack(fill="x", pady=(0, 10))

        # Foto de Perfil
        profile_label = tk.Label(self.info_frame, image=self.images.get('profile'), bg=BG_MAIN)
        if self.images.get('profile'):
            profile_label.image = self.images.get('profile')
        else:
            profile_label.config(text="Foto", bg="#555555", width=10, height=5)

        profile_label.pack(side="top", anchor="w", pady=(0, 5))

        # Nome Completo
        name_label = tk.Label(self.info_frame, text=self.user_data.get('name', 'Nome do Usuário'),
                              fg=TEXT_COLOR, bg=BG_MAIN, font=("Arial", 16, "bold"), anchor="w")
        name_label.pack(fill="x", pady=(5, 0))
        
        # Username (@)
        username_label = tk.Label(self.info_frame, text=f"@{self.user_data.get('username', 'usuario_mock')}",
                                  fg=SUBTEXT_COLOR, bg=BG_MAIN, font=("Arial", 11), anchor="w")
        username_label.pack(fill="x", pady=(0, 5))

        # --- Botões de Ação Dinâmicos Seguir e Editar ---
        self.action_frame = tk.Frame(header_row, bg=BG_MAIN)
        self.action_frame.pack(side="right", anchor="center", pady=(10, 0))

        self.follow_button = tk.Button(self.action_frame, text="Seguir", image=self.images.get('follow'), compound="left",
                                   command=self._on_follow_click,
                                   bg=ACCENT_COLOR, fg=TEXT_COLOR, activebackground=ACCENT_COLOR,
                                   activeforeground=TEXT_COLOR, relief="flat", font=("Arial", 9, "bold"),
                                   padx=10, pady=4)
        if self.images.get('follow'):
            self.follow_button.image = self.images.get('follow')
        self.follow_button.pack(side="left")

        # Botão Editar
        self.edit_button = tk.Button(self.action_frame, text="Editar", command=self._toggle_edit_mode,
                                     bg="#555555", fg=TEXT_COLOR, activebackground="#777777",
                                     relief="flat", font=("Arial", 9, "bold"), padx=10, pady=4)
        self.edit_button.pack(side="left", padx=(10, 0))
        # Fim dos Botões de Ação Dinâmicos

        # --- 3. Detalhes  ---
        details_frame = tk.Frame(self.info_frame, bg=BG_MAIN)
        details_frame.pack(fill="x", pady=5)

        location_label = tk.Label(details_frame, image=self.images.get('location'), compound="left",
                                   text=self.user_data.get('location', 'Osasco - SP'),
                                   fg=SUBTEXT_COLOR, bg=BG_MAIN, font=("Arial", 9))
        if self.images.get('location'):
            location_label.image = self.images.get('location')
        location_label.pack(side="left", padx=(0, 10))

        education_label = tk.Label(details_frame, image=self.images.get('education'), compound="left",
                                    text=self.user_data.get('education', 'Fatec Carapicuiba'),
                                    fg=SUBTEXT_COLOR, bg=BG_MAIN, font=("Arial", 9))
        if self.images.get('education'):
            education_label.image = self.images.get('education')
        education_label.pack(side="left")

        # ---  Abas de Conteúdo  ---
        style = ttk.Style()
        style.theme_create("CustomStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": BG_MAIN}},
            "TNotebook.Tab": {
                "configure": {"padding": [10, 4], "background": BG_MAIN, "foreground": SUBTEXT_COLOR, "font": ('Arial', 9, 'bold')},
                "map": {"background": [("selected", BG_MAIN)], "foreground": [("selected", ACCENT_COLOR)]}
            }
        })
        style.theme_use("CustomStyle")

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, sticky="nsew", padx=15, pady=(5, 0))

        self.about_frame = tk.Frame(self.notebook, bg=BG_MAIN, padx=10, pady=10)
        self.notebook.add(self.about_frame, text="Sobre")
        self._create_about_tab(self.about_frame)

        activity_frame = tk.Frame(self.notebook, bg=BG_MAIN, padx=10, pady=10)
        self.notebook.add(activity_frame, text="Atividade")
        self._create_activity_tab(activity_frame)

    def _show_temp_banner(self, message, color):
        """Exibe um banner temporário com uma mensagem no topo da tela."""
        if self.banner_id:
            self.after_cancel(self.banner_id)
        
        self.banner_frame.config(bg=color)
        self.banner_label.config(text=message, bg=color)
        
        # Coloca o banner acima de todo o conteúdo da tela
        self.banner_frame.lift()
        self.banner_frame.grid(row=0, column=0, columnspan=1, sticky="ew", pady=0)
        self.banner_frame.grid_configure(row=0, columnspan=1, sticky="ew")

        # Oculta o banner após 2.5 segundos
        self.banner_id = self.after(2500, self._hide_banner)

    def _hide_banner(self):
        """Oculta o banner de notificação."""
        if self.banner_frame.winfo_ismapped():
            self.banner_frame.grid_forget()

    def _create_about_tab(self, parent_frame):
        # Limpa o frame para reconstrução no modo de edição
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # --- Interesses ---
        interests_title = tk.Label(parent_frame, text="Interesses", fg=TEXT_COLOR, bg=BG_MAIN, font=("Arial", 11, "bold"), anchor="w")
        interests_title.pack(fill="x", pady=(0, 5))

        if self.is_editing:
            # Modo de Edição
            self.interests_entry = tk.Entry(parent_frame, textvariable=self.interests_var,
                                            bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                                            relief="flat", bd=0, font=("Arial", 10), justify='left')
            self.interests_entry.pack(fill="x", pady=(0, 10))
        else:
            # Modo de Visualização
            tags_frame = tk.Frame(parent_frame, bg=BG_MAIN)
            tags_frame.pack(fill="x", pady=(0, 10))

            # Converte a string de interesses (separada por vírgula) em tags
            interests_list = [tag.strip() for tag in self.interests_var.get().split(',') if tag.strip()]
            
            for text in interests_list:
                tag_label = tk.Label(tags_frame, text=text, bg=ACCENT_COLOR, fg=TEXT_COLOR, padx=6, pady=2, relief="flat", font=("Arial", 9))
                tag_label.pack(side="left", padx=(0, 6))

        # --- Descrição ---
        desc_title = tk.Label(parent_frame, text="Descrição", fg=TEXT_COLOR, bg=BG_MAIN, font=("Arial", 11, "bold"), anchor="w")
        desc_title.pack(fill="x", pady=(0, 5))

        if self.is_editing:
            # Modo de Edição
            self.description_text_widget = tk.Text(parent_frame, height=5,
                                                   bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                                                   relief="flat", bd=0, font=("Arial", 10), wrap="word")
            self.description_text_widget.insert("1.0", self.description_var.get())
            self.description_text_widget.pack(fill="x", expand=False)
        else:
            # Modo de Visualização
            desc_label = tk.Label(parent_frame, text=self.description_var.get(), fg=SUBTEXT_COLOR, bg=BG_MAIN, font=("Arial", 9), justify="left", wraplength=350, anchor="nw")
            desc_label.pack(fill="both", expand=True)

        # Botão Salvar
        if self.is_editing:
            save_button = tk.Button(parent_frame, text="Salvar Alterações", command=self._on_save_click,
                                    bg=ACCENT_COLOR, fg=TEXT_COLOR, activebackground=ACCENT_COLOR,
                                    relief="flat", font=("Arial", 10, "bold"), padx=10, pady=5)
            save_button.pack(fill="x", pady=(15, 0))


    def _create_activity_tab(self, parent_frame):
        post_label = tk.Label(parent_frame, text="Feed de Posts e Projetos aqui...", fg=SUBTEXT_COLOR, bg=BG_MAIN, font=("Arial", 9))
        post_label.pack(fill="both", expand=True)

    def _toggle_edit_mode(self):
        """Alterna entre os modos de visualização e edição"""
        self.is_editing = not self.is_editing
        
        if self.is_editing:
            self.edit_button.config(text="Cancelar Edição", bg="#F44336")
            self.follow_button.pack_forget()
            print("DEBUG: Entrou no Modo de Edição.")
        else:
            self.edit_button.config(text="Editar", bg="#555555")
            self.follow_button.pack(side="left")
            print("DEBUG: Saiu do Modo de Edição (Sem Salvar).")

        # Recria a aba "Sobre" para exibir os novos widgets
        self._create_about_tab(self.about_frame)
        self.notebook.select(self.about_frame)

    def _on_save_click(self):
        """Salva as alterações e sai do modo de edição."""
        #  Captura os novos valores
        new_description = self.description_text_widget.get("1.0", "end-1c").strip()
        self.description_var.set(new_description)

        new_interests_string = self.interests_var.get().strip()

        # Atualiza os dados (Simulação de salvamento)
        self.user_data['description'] = new_description
        self.user_data['interests'] = new_interests_string

        print(f"DEBUG: Dados Salvos! Descrição: '{new_description}' | Interesses (raw): '{new_interests_string}'")
        self._show_temp_banner("Perfil salvo com sucesso!", SUCCESS_COLOR)

        # Sai do modo de edição
        self._toggle_edit_mode()

    def _on_follow_click(self):
        """Função chamada ao clicar no botão Seguir."""
        user_to_follow = self.user_data.get('name', 'o usuário')
        self._show_temp_banner(f"Você seguiu {user_to_follow}!", SUCCESS_COLOR)
        # Aqui você implementaria a lógica real de seguir/deixar de seguir
        print("DEBUG: Clicou em Seguir")

    def _on_back_click(self):
        
        # Exibe a mensagem de função de navegação antes de chamar o callback
        self._show_temp_banner("Função para ir para a Home/Feed", "#3498DB") #

        # Em uma aplicação real, você chamaria o callback após um pequeno atraso
       
        self.after(500, self.navigate_back_callback)


if __name__ == "__main__":
    # Dados de exemplo 
    mock_user_data = {
        'name': 'Alan Oliveira',
        'username': 'alandev', # Adicionado
        'location': 'Concordia - SC',
        'education': 'IFC - Concordia',
        'interests': ["Design", "Marketing", "Fotografia"], 
        'description': 'Arte é minha maior paixão, eu sou gamada em Fotografia e Design...Marketing também haha me adiciona aí para conversarmos! :)'
    }

    def go_back():
        print("DEBUG: Navegar de volta (saindo da tela de perfil)")
        # root.quit() # Comentado para permitir que o banner temporário seja visto

    root = tk.Tk()
    root.title("Perfil do Usuário (Mobile)")
    root.geometry(f"{MOBILE_WIDTH}x{MOBILE_HEIGHT}")
    root.resizable(False, False)
    root.config(bg=BG_MAIN)

    app = UserProfileView(root, mock_user_data, go_back)
    app.pack(fill="both", expand=True)

    root.mainloop()