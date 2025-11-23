import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk 
import tkinter.font as tkFont 
from .config_layout import *
from ..config.settings import (
    DARK_THEME_COLORS, carregar_icone, font_roboto, 
    font_inter, font_roboto_big, on_entry_click, on_focus_out
)

# Importa o novo controller de perfil E as novas funções de atualização
from ..controller.profileController import load_user_profile_data, update_user_bio, update_user_interests

def abrir_home(usuario, login_root): 
    """Cria e exibe a tela Home, e carrega os dados do perfil."""

    # CORREÇÃO DA FONTE: Cria a fonte aqui, APÓS a inicialização do Tkinter
    try:
        font_inter_small = tkFont.Font(family="Inter", size=10)
    except Exception:
        font_inter_small = tkFont.Font(family="Arial", size=10) # Fallback

    # 1. Carrega dados do perfil (com os novos padrões)
    profile_data = load_user_profile_data(usuario)
    if not profile_data:
        # Fallback se os dados não carregarem
        profile_data = {
            "username": usuario, "bio": "Bio padrão. Edite seu perfil!",
            "location": "Concórdia - SC", "education": "IFC Concórdia",
            "interests": ["Tecnologia", "Inovação", "Codificação"], "posts": []
        }
        

    # Função de Logout
    def fazer_logout():
        home.destroy(); login_root.deiconify(); messagebox.showinfo("Logout", "Sessão encerrada com sucesso.")

   

    # --- Conteúdo da Aba HOME (Feed de Posts) ---
    f = frames["Home"]
    tk.Label(f, text="Feed de Posts", font=font_roboto_big, bg=colors["bg_frame"], fg=colors["fg_text"]).pack(pady=10)
    feed = scrolledtext.ScrolledText(f, width=42, height=20, font=font_inter, bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"], wrap="word") 
    feed.insert("end", "Nenhuma publicação ainda..."); feed.configure(state="disabled"); feed.pack(padx=10, pady=5, fill="both", expand=True)

    # Função Publicar
    def publicar():
        texto = post_box.get("1.0", "end-1c").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite algo antes de publicar."); return
        feed.configure(state="normal"); feed.insert("1.0", f"\n\n{usuario}: {texto}\n{'-'*40}\n")
        feed.configure(state="disabled"); post_box.delete("1.0", "end"); messagebox.showinfo("OK", "Publicado!")

   

    # --- Conteúdo da Aba RANKING e PROJETOS ---
    
    

    # --- Conteúdo da Aba PERFIL ---
    f_perfil = frames["Perfil"] 
    
    # Frame para o banner de capa
    cover_frame = tk.Frame(f_perfil, bg=colors["bg_frame"])
    cover_frame.pack(fill="x")
    cover_label = tk.Label(cover_frame, image=icones["cover_image"] or tk.Frame(cover_frame, height=150, bg="lightgray"), bg=colors["bg_frame"])
    cover_label.pack(fill="x", expand=True)

    # CORREÇÃO TclError: Substitui "transparent" por colors["bg_frame"]
    if icones["back_arrow"]:
        tk.Button(cover_frame, image=icones["back_arrow"], 
                  command=lambda: mostrar_aba_principal("Home"), 
                  bg=colors["bg_frame"],                 # <<-- CORRIGIDO
                  activebackground=colors["bg_frame"],  # <<-- CORRIGIDO
                  bd=0, highlightthickness=0, relief="flat") \
                  .place(x=10, y=10) 

    # Frame para a foto de perfil e informações básicas
    info_frame = tk.Frame(f_perfil, bg=colors["bg_main"], padx=20, pady=10); info_frame.pack(fill="x")

    # Foto de Perfil
    if icones["profile_pic"]:
        profile_pic_label = tk.Label(info_frame, image=icones["profile_pic"], bg=colors["bg_main"])
        profile_pic_label.place(x=0, y=-50) 
    
    # Nome do Usuário
    tk.Label(info_frame, text=profile_data["username"], font=font_roboto_big, 
             bg=colors["bg_main"], fg=colors["fg_text"]).pack(anchor="w", padx=(100,0))

    # Ícone de Amigos
    if icones["friends_icon"]:
        tk.Label(info_frame, image=icones["friends_icon"], bg=colors["bg_main"]).place(x=360, y=5)

    # Localização e Formação (Agora com valores padrão: IFC Concórdia)
    location_edu_frame = tk.Frame(info_frame, bg=colors["bg_main"]); location_edu_frame.pack(fill="x", pady=5, anchor="w", padx=(100,0))
    
    if icones["location_icon"]:
        tk.Label(location_edu_frame, image=icones["location_icon"], bg=colors["bg_main"]).pack(side="left", padx=(0,2))
    tk.Label(location_edu_frame, text=profile_data["location"], font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(side="left", padx=(0,10))

    if icones["education_icon"]:
        tk.Label(location_edu_frame, image=icones["education_icon"], bg=colors["bg_main"]).pack(side="left", padx=(0,2))
    tk.Label(location_edu_frame, text=profile_data["education"], font=font_inter, bg=colors["bg_main"], fg=colors["fg_text"]).pack(side="left")

    # --- Sub-abas "Sobre" e "Atividade" ---
    sub_aba_frame = tk.Frame(f_perfil, bg=colors["bg_main"], pady=10); sub_aba_frame.pack(fill="x")

    sub_abas = ["Sobre", "Atividade"]; sub_aba_botoes = []
    conteudo_sub_abas = {};
    for sa in sub_abas:
        conteudo_sub_abas[sa] = tk.Frame(f_perfil, bg=colors["bg_frame"], padx=10, pady=10)

    def mostrar_sub_aba(aba_selecionada):
        for sa_btn in sub_aba_botoes:
            sa_btn.config(bg=colors["bg_frame"], fg=colors["fg_text"])
        for sa_btn in sub_aba_botoes:
            if sa_btn.cget("text") == aba_selecionada:
                sa_btn.config(bg=colors["purple_button"], fg=colors["fg_button"])

        for sa_frame in conteudo_sub_abas.values(): sa_frame.pack_forget()
        conteudo_sub_abas[aba_selecionada].pack(fill="both", expand=True, padx=10, pady=5)
    
    for sa in sub_abas:
        btn = tk.Button(sub_aba_frame, text=sa, font=font_inter, command=lambda a=sa: mostrar_sub_aba(a),
                        bd=0, highlightthickness=0, relief="flat", padx=15, pady=5); btn.pack(side="left", padx=5)
        sub_aba_botoes.append(btn)
    
    
    # --- Conteúdo da Sub-aba "Sobre" (AGORA EDITÁVEL) ---
    f_sobre = conteudo_sub_abas["Sobre"]
    
    # --- Funções de Edição para o Perfil ---
    
    def salvar_bio():
        """Salva o novo texto da biografia (chama o controller)."""
        nova_bio = bio_text_area.get("1.0", "end-1c").strip()
        update_user_bio(usuario, nova_bio)
        
    def add_interest():
        """Adiciona um novo interesse (tag) e recarrega a visualização das tags."""
        novo_interesse = interest_entry.get().strip()
        interest_entry.delete(0, tk.END)
        
        if novo_interesse and novo_interesse not in profile_data["interests"]:
            profile_data["interests"].append(novo_interesse)
            update_user_interests(usuario, profile_data["interests"]) # Salva a nova lista
            draw_interests() # Atualiza a UI

    def remove_interest(tag_to_remove):
        """Remove um interesse (tag) e recarrega a visualização das tags."""
        if tag_to_remove in profile_data["interests"]:
            profile_data["interests"].remove(tag_to_remove)
            update_user_interests(usuario, profile_data["interests"]) # Salva a nova lista
            draw_interests() # Atualiza a UI
            
    # Função que desenha as tags dinamicamente
    def draw_interests():
        # Limpa o frame de tags existente
        for widget in tags_frame.winfo_children():
            widget.destroy()

        for interesse in profile_data["interests"]:
            # Cria um frame para a tag e o botão 'x'
            tag_box = tk.Frame(tags_frame, bg=colors["purple_button"], padx=0, pady=0)
            tag_box.pack(side="left", padx=(5, 0), pady=4)
            
            # Label com o nome do interesse
            tk.Label(tag_box, text=interesse, font=font_inter_small, 
                     bg=colors["purple_button"], fg=colors["fg_button"], padx=4, pady=2, relief="flat", bd=0) \
              .pack(side="left", padx=(4, 0))

            # Botão para remover a tag
            tk.Button(tag_box, text="x", font=font_inter_small, 
                      command=lambda tag=interesse: remove_interest(tag),
                      bg=colors["purple_button"], fg=colors["fg_button"], bd=0, relief="flat",
                      activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"], padx=4) \
              .pack(side="left", padx=(0, 4))
              

    # --- Área de Edição da BIO/DESCRIÇÃO ---
    tk.Label(f_sobre, text="Descrição (Editável)", font=font_roboto, bg=colors["bg_frame"], fg=colors["fg_text"]).pack(pady=(10,5), anchor="w")
    
    bio_text_area = scrolledtext.ScrolledText(f_sobre, height=5, width=40, font=font_inter_small,
                                         bg=colors["bg_entry"], fg=colors["fg_entry"], wrap="word",
                                         insertbackground=colors["fg_entry"])
    bio_text_area.insert("1.0", profile_data["bio"]) # Insere a bio carregada
    bio_text_area.pack(pady=5, anchor="w", fill="x")
    
    tk.Button(f_sobre, text="Salvar Descrição", command=salvar_bio, font=font_inter_small,
              bg=colors["bg_button"], fg=colors["fg_button"],
              activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"]).pack(pady=5, anchor="e")

    # --- Área de Edição de INTERESSES ---
    tk.Label(f_sobre, text="Interesses (Tags)", font=font_roboto, bg=colors["bg_frame"], fg=colors["fg_text"]).pack(pady=(10,5), anchor="w")
    
    # Frame onde as tags serão desenhadas dinamicamente
    tags_frame = tk.Frame(f_sobre, bg=colors["bg_frame"])
    tags_frame.pack(fill="x", pady=5, anchor="w")
    
    # Desenha as tags iniciais
    draw_interests() 
    
    # Campo de entrada e botão para adicionar novo interesse
    add_interest_frame = tk.Frame(f_sobre, bg=colors["bg_frame"])
    add_interest_frame.pack(fill="x", pady=10)
    
    interest_entry = tk.Entry(add_interest_frame, width=30, font=font_inter_small,
                              bg=colors["bg_entry"], fg=colors["fg_entry"], insertbackground=colors["fg_entry"])
    interest_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    tk.Button(add_interest_frame, text="Adicionar", command=add_interest, font=font_inter_small,
              bg=colors["purple_button"], fg=colors["fg_button"],
              activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"]).pack(side="right")
    
    
    # Botão de Logout (no final da aba)
    tk.Button(f_sobre, text="Logout", command=fazer_logout, font=font_inter,
              bg=colors["bg_button"], fg=colors["fg_button"],
              activebackground=colors["active_bg_button"], activeforeground=colors["fg_button"]).pack(pady=20)
              
    # --- Conteúdo da Sub-aba "Atividade" ---
    f_atividade = conteudo_sub_abas["Atividade"]
    atividade_scroll_frame = scrolledtext.ScrolledText(f_atividade, width=45, height=25, font=font_inter,
                                                    bg=colors["bg_frame"], fg=colors["fg_text"], wrap="word", bd=0, highlightthickness=0); atividade_scroll_frame.pack(fill="both", expand=True)
    
    atividade_scroll_frame.config(state="normal")
    for post in profile_data["posts"]:
        atividade_scroll_frame.insert("end", f"{profile_data['username']}\n")
        atividade_scroll_frame.insert("end", post["text"] + "\n\n", "post_text")
        if post.get("has_image") and icones["post_image"]:
            atividade_scroll_frame.image_create("end", image=icones["post_image"])
            atividade_scroll_frame.insert("end", "\n")
        atividade_scroll_frame.insert("end", "\n" + "-"*50 + "\n\n")

    atividade_scroll_frame.config(state="disabled")
    atividade_scroll_frame.image_refs = [icones["post_image"]] 


    # --- Lógica da Barra de Navegação Inferior ---
    def mostrar_aba_principal(aba):
        for fr in frames.values(): fr.pack_forget()
        frames[aba].pack(fill="both", expand=True)
        
        for btn in botoes_barra:
            btn.config(fg=colors["icon_active_fg"] if btn.cget("text") == aba else colors["icon_inactive_fg"],
                       activeforeground=colors["icon_active_fg"] if btn.cget("text") == aba else colors["icon_inactive_fg"])

        if aba == "Perfil": mostrar_sub_aba("Sobre")
        
    barra_frame = tk.Frame(home, bg=colors["bg_main"]); barra_frame.pack(side="bottom", fill="x", padx=0)
    barra = tk.Frame(barra_frame, bg=colors["bottom_bar_bg"], height=60, relief="flat", bd=0, padx=5, pady=5); barra.pack(fill="x")

    for aba in abas_principais:
        icone = icones.get(aba)
        initial_fg = colors["icon_active_fg"] if aba == "Home" else colors["icon_inactive_fg"]
        btn = tk.Button(barra, text=aba, image=icone, compound='top', width=60, command=lambda a=aba: mostrar_aba_principal(a), font=("Inter", 9), bd=0, highlightthickness=0, bg=colors["bottom_bar_bg"], fg=initial_fg, activebackground=colors["bottom_bar_bg"], activeforeground=initial_fg)
        btn.pack(side="left", expand=True, fill="x", padx=5); botoes_barra.append(btn) 
    
    home.image_refs = list(icones.values()) 
    mostrar_aba_principal("Home")