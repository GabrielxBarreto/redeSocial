import tkinter as tk
from tkinter import scrolledtext, messagebox

# Importação direta (sem ponto) para funcionar como script autônomo
# É ESSENCIAL que utils_icons.py esteja com a versão mais recente!
from utils_icons import (
    colors, font_roboto_big, font_inter, 
    setup_test_window
)

def criar_aba_novo_post(container_frame, icones):
    """
    Cria e retorna o frame da aba Novo Post.

    Args:
        container_frame (tk.Widget): O widget pai onde o frame será colocado.
        icones (dict): Dicionário contendo os ícones carregados (não usado diretamente, mas passado para fins de consistência).

    Returns:
        tk.Frame: O frame da aba Novo Post.
    """
    
    f = tk.Frame(container_frame, bg=colors["bg_frame"])
    f.grid_rowconfigure(2, weight=1) # Faz com que a área de conteúdo ocupe o espaço
    f.grid_columnconfigure(0, weight=1)

    # Título da Tela
    tk.Label(f, text="Criar Novo Post", font=font_roboto_big, bg=colors["bg_frame"], fg=colors["fg_text"]).grid(row=0, column=0, pady=10, sticky="ew")

    # Frame de entrada de dados (ocupa a maior parte do espaço)
    form_frame = tk.Frame(f, bg=colors["bg_frame"])
    form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    form_frame.grid_columnconfigure(0, weight=1)
    
    # Faz com que a área de texto dentro do form_frame se expanda
    form_frame.grid_rowconfigure(3, weight=1) 

    # Label e Campo para Título/Assunto
    tk.Label(form_frame, text="Título/Assunto:", bg=colors["bg_frame"], fg=colors["fg_text"], font=font_inter).grid(row=0, column=0, sticky="w", pady=(0, 5))
    title_entry = tk.Entry(form_frame, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"], font=font_inter, relief="flat")
    title_entry.grid(row=1, column=0, sticky="ew", ipady=5)

    # Label e Área de Texto para Conteúdo
    tk.Label(form_frame, text="Conteúdo:", bg=colors["bg_frame"], fg=colors["fg_text"], font=font_inter).grid(row=2, column=0, sticky="w", pady=(15, 5))
    content_text = scrolledtext.ScrolledText(form_frame, height=10, width=40, font=font_inter,
                                             bg=colors["bg_entry"], fg=colors["fg_entry"], 
                                             insertbackground=colors["fg_entry"], wrap="word", relief="flat", borderwidth=0, highlightthickness=0)
    content_text.grid(row=3, column=0, sticky="nsew")
    
    # Botão para Anexar Imagem (Mock)
    def anexar_imagem():
        messagebox.showinfo("Anexar Imagem (Mock)", "Função para anexar imagem será implementada na camada de Controller.")

    btn_image = tk.Button(form_frame, text="Anexar Imagem", command=anexar_imagem,
                          bg=colors["bg_button"], fg=colors["fg_text"], 
                          activebackground=colors["active_bg_button"], relief="flat", 
                          font=font_inter)
    btn_image.grid(row=4, column=0, sticky="ew", pady=(15, 5))

    # Botão Publicar
    def publicar_post():
        titulo = title_entry.get().strip()
        conteudo = content_text.get("1.0", tk.END).strip()
        
        if not titulo or not conteudo:
            messagebox.showerror("Erro de Publicação", "Título e Conteúdo não podem estar vazios.")
            return

        # Mock de publicação: Simula o que um Controller faria
        messagebox.showinfo("Sucesso", f"Postagem '{titulo}' publicada!\nConteúdo: {conteudo[:50]}...")
        
        # Limpar campos após a publicação
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        
    btn_publicar = tk.Button(f, text="PUBLICAR", command=publicar_post,
                             bg=colors["purple_button"], fg=colors["fg_text"], 
                             activebackground=colors["active_bg_button"], relief="flat", 
                             font=font_roboto_big, height=2)
    # sticky="sEW" para grudar no fundo e expandir horizontalmente
    btn_publicar.grid(row=2, column=0, sticky="sEW", padx=20, pady=(0, 20)) 
    
    return f

# --- BLOCO DE TESTE INDIVIDUAL ---
if __name__ == "__main__":
    # Garante que setup_test_window retorna 3 valores (test_window, root, icones_mock)
    test_window, root, icones_mock = setup_test_window("Teste Individual: Novo Post") 
    
    # Passa os ícones carregados para a função de criação da aba
    frame = criar_aba_novo_post(test_window, icones_mock)
    frame.pack(fill="both", expand=True)
    
    root.mainloop()