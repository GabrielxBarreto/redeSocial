import tkinter as tk
from tkinter import scrolledtext, messagebox
if __package__:
    from redesocial.service.userService import new_post
else:
    from redesocial.service.userService import new_post

from redesocial.views.utils_icons import colors, font_roboto_big, font_inter, setup_test_window

if "accent_color" not in colors:
    colors["accent_color"] = "#6f42c1" 
if "accent_color_hover" not in colors:
    colors["accent_color_hover"] = "#5a369a"
class NovoPostView(tk.Frame):
    """
    Tela/Frame para criar um novo post.
    Pode ser chamado pelo main.py com switch_view.
    """
    global session_global

    def __init__(self, master, icones=None, session=None, switch_view_callback = None,*args, **kwargs):
        super().__init__(master, bg=colors["bg_frame"], *args, **kwargs)
        self.switch_view_callback = switch_view_callback
        self.icones = icones or {}
        self.session = session  # id de usuário/logado (mock)
        session_global = self.session
        self.pack_propagate(False)
        self._create_widgets()

    def _create_widgets(self):
        # Título da Tela
        tk.Label(self, text="Criar Novo Post", font=font_roboto_big, bg=colors["bg_frame"], fg=colors["fg_text"]).grid(row=0, column=0, pady=10, sticky="ew")

        # Frame de formulário
        form_frame = tk.Frame(self, bg=colors["bg_frame"])
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(3, weight=1)  # para expandir área de texto

        # Campo Título
        tk.Label(form_frame, text="Título/Assunto:", bg=colors["bg_frame"], fg=colors["fg_text"], font=font_inter).grid(row=0, column=0, sticky="w", pady=(0,5))
        self.title_entry = tk.Entry(form_frame, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"], font=font_inter, relief="flat")
        self.title_entry.grid(row=1, column=0, sticky="ew", ipady=5)

        # Campo Conteúdo
        tk.Label(form_frame, text="Conteúdo:", bg=colors["bg_frame"], fg=colors["fg_text"], font=font_inter).grid(row=2, column=0, sticky="w", pady=(15,5))
        self.content_text = scrolledtext.ScrolledText(form_frame, height=10, width=40, font=font_inter,
                                                      bg=colors["bg_entry"], fg=colors["fg_entry"],
                                                      insertbackground=colors["fg_entry"], wrap="word", relief="flat", borderwidth=0, highlightthickness=0)
        self.content_text.grid(row=3, column=0, sticky="nsew")

        # Botão Anexar Imagem (mock)
        btn_image = tk.Button(form_frame, text="Anexar Imagem", command=self.anexar_imagem,
                              bg=colors["bg_button"], fg=colors["fg_text"],
                              activebackground=colors["active_bg_button"], relief="flat",
                              font=font_inter)
        btn_image.grid(row=4, column=0, sticky="ew", pady=(15,5))

        # Botão Publicar
        btn_publicar = tk.Button(self, text="PUBLICAR", command=self.publicar_post,
                                 bg=colors["purple_button"], fg=colors["fg_text"],
                                 activebackground=colors["active_bg_button"], relief="flat",
                                 font=font_roboto_big, height=2)
        btn_publicar.grid(row=2, column=0, sticky="sEW", padx=20, pady=(0,20))
        btn_voltar = tk.Button(self, text="⬅ Voltar para Home", command=self._voltar_home,
                       bg=colors.get("accent_color", "#6f42c1"),
                       fg=colors.get("fg_text", "#ffffff"),
                       activebackground=colors.get("accent_color_hover", "#5a369a"),
                       font=font_roboto_big, height=2, relief="flat", cursor="hand2")
        btn_voltar.grid(row=3, column=0, sticky="sEW", padx=20, pady=(0,20))
    def _voltar_home(self):
        """Chama a callback para voltar para Home."""
        if self.switch_view_callback:
            self.switch_view_callback("home")
        else:
            messagebox.showinfo("Navegação Mock", "Voltando para a Home!")
    def anexar_imagem(self):
        """Mock: função para anexar imagem."""
        messagebox.showinfo("Anexar Imagem (Mock)", "Função para anexar imagem será implementada na camada de Controller.")

    def publicar_post(self):
        """Valida e publica o post chamando o service."""
        titulo = self.title_entry.get().strip()
        conteudo = self.content_text.get("1.0", tk.END).strip()

        if not titulo or not conteudo:
            messagebox.showerror("Erro de Publicação", "Título e Conteúdo não podem estar vazios.")
            return
        
        archive = None  # mock de arquivo
        new_post(session_global, archive, f"{titulo}:{conteudo}")

        messagebox.showinfo("Sucesso", f"Postagem '{titulo}' publicada!\nConteúdo: {conteudo[:50]}...")

        # Limpar campos
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)


# --- BLOCO DE TESTE INDIVIDUAL ---
if __name__ == "__main__":
    test_window, root, icones_mock = setup_test_window("Teste Individual: Novo Post")

    frame = NovoPostView(test_window, icones_mock)
    frame.pack(fill="both", expand=True)

    root.mainloop()
