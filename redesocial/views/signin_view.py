import tkinter as tk
from tkinter import messagebox
import sys
import traceback
from redesocial.controller.authController import loginController

#  Defis de Fallback 



SOLID_GRAY_BLOCK = "#3C3C3C" 

FALLBACK_COLORS = {
    "bg_main": "#1e1e1e",           # Fundo Principal Escuro
    "fg_text": "#ffffff",           # Texto Principal Branco
    "accent_color": "#6f42c1",      # Roxo (Mantido para o botão LOGIN)
    "accent_color_hover": "#5a369a", # Roxo mais escuro para hover
    "bg_entry": SOLID_GRAY_BLOCK,   # Fundo do campo de entrada (Cinza Sólido)
    "bg_entry_border": SOLID_GRAY_BLOCK, # Borda deve ser a mesma cor, ou não ser usada
    "fg_secondary": "#aaaaaa",      # Cinza claro para placeholder e texto auxiliar
    "icon_active_fg": SOLID_GRAY_BLOCK, # Cinza Sólido para ícone de senha (ativo/inativo)
    "signup_link_fg": "#6f42c1",    # ROXO Cor do link de cadastro
    "signup_link_active_fg": "#5a369a", 
}
FALLBACK_FONT_BIG = ("Roboto", 18, "bold")
FALLBACK_FONT_DEFAULT = ("Roboto", 12)
FALLBACK_FONT_SMALL = ("Inter", 10)
FALLBACK_WIDTH, FALLBACK_HEIGHT = 400, 600

# import do utils_icons, definindo fallbacks se a importação falhar
try:
    from utils_icons import (
        colors,
        font_roboto_big,
        font_roboto,
        font_inter_small,
        FRAME_WIDTH,
        FRAME_HEIGHT,
        setup_test_window
    )
    
   
    colors["bg_entry"] = FALLBACK_COLORS["bg_entry"]
    colors["bg_entry_border"] = FALLBACK_COLORS["bg_entry_border"]
    colors["icon_active_fg"] = FALLBACK_COLORS["icon_active_fg"]   
    colors["fg_secondary"] = FALLBACK_COLORS["fg_secondary"] # Placeholder mais claro
    
    # SOBRESCRITAS DO LINK DE CADASTRO PARA ROXO
    colors["signup_link_fg"] = FALLBACK_COLORS["signup_link_fg"] 
    colors["signup_link_active_fg"] = FALLBACK_COLORS["signup_link_active_fg"] 

    
    if "accent_color" not in colors:
        colors["accent_color"] = FALLBACK_COLORS["accent_color"]
    if "accent_color_hover" not in colors:
        colors["accent_color_hover"] = FALLBACK_COLORS["accent_color_hover"]

except ImportError:
    # Se o utils_icons falhar completamente, usamos os fallbacks
    print("Aviso: Falha ao importar utils_icons.py. Usando cores e fontes padrão.")
    colors = FALLBACK_COLORS
    font_roboto_big = FALLBACK_FONT_BIG
    font_roboto = FALLBACK_FONT_DEFAULT
    font_inter_small = FALLBACK_FONT_SMALL
    FRAME_WIDTH = FALLBACK_WIDTH
    FRAME_HEIGHT = FALLBACK_HEIGHT
    setup_test_window = None


# Componente customizado para o Campo de Entrada

class CustomEntry(tk.Frame):
    """
    Frame customizado que envolve um Label e um Entry para um visual limpo e moderno.
    Agora usa um Entry com fundo de cor sólida.
    """
    def __init__(self, master, label_text, placeholder="", is_password=False, **kwargs):
        super().__init__(master, bg=colors["bg_main"], **kwargs)
        self.label_text = label_text
        self.placeholder = placeholder
        self.is_password = is_password
        self.show_password = not is_password
        self.var = tk.StringVar()
        
        self.entry_block_color = colors.get("bg_entry", FALLBACK_COLORS["bg_entry"]) 
        
        self._create_widgets()

    def _create_widgets(self):
        
        
        tk.Label(self,
                 text=self.label_text,
                 font=font_roboto,
                 bg=colors["bg_main"],
                 fg=colors["fg_text"],
                 anchor="w").pack(fill="x", pady=(5, 2))

        # Frame Container para o Entry e o Botão
        entry_container = tk.Frame(self, bg=self.entry_block_color, height=40)
        entry_container.pack(fill="x", pady=(0, 15))
        entry_container.pack_propagate(False)

        # Campo de Entrada
        self.entry_widget = tk.Entry(entry_container,
                                     textvariable=self.var,
                                     font=font_roboto,
                                     bg=self.entry_block_color,
                                     fg=colors["fg_text"],
                                     insertbackground=colors["fg_text"],
                                     bd=0,
                                     highlightthickness=0)
        
        if self.is_password:
            self.entry_widget.config(show="*" if not self.show_password else "")
        
    
        self.entry_widget.insert(0, self.placeholder)
        
        # Placeholder em cinza claro
        self.entry_widget.config(fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]))
        
        self.entry_widget.bind("<FocusIn>", self._clear_placeholder)
        self.entry_widget.bind("<FocusOut>", self._restore_placeholder)
        
        
        entry_xpad = 5
        if self.is_password:
            
            self.entry_widget.pack(side=tk.LEFT, fill="x", expand=True, padx=(entry_xpad, 0))
            self._create_password_toggle_button(entry_container)
        else:
            self.entry_widget.pack(side=tk.LEFT, fill="x", expand=True, padx=(entry_xpad, 5))

    def _clear_placeholder(self, event):
        """Limpa o placeholder quando o campo recebe foco."""
        if self.entry_widget.get() == self.placeholder:
            self.entry_widget.delete(0, tk.END)
            self.entry_widget.config(fg=colors["fg_text"])
            
            
            if self.is_password and not self.show_password:
                self.entry_widget.config(show="*")

    def _restore_placeholder(self, event):
        """Restaura o placeholder se o campo for perdido e estiver vazio."""
        if not self.entry_widget.get():
            self.entry_widget.insert(0, self.placeholder)
            self.entry_widget.config(fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]))
            
            
            if self.is_password:
                self.entry_widget.config(show="")

    def _create_password_toggle_button(self, master):
        """Cria o botão de mostrar/esconder senha."""
        
        self.toggle_btn = tk.Label(master,
                                   text="👁️",
                                   font=("Arial", 14),
                                   bg=self.entry_block_color,
                                 
                                   fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]),
                                   cursor="hand2")
        self.toggle_btn.bind("<Button-1>", self._toggle_password_visibility)
        self.toggle_btn.pack(side=tk.RIGHT, padx=5)

    def _toggle_password_visibility(self, event):
        """Alterna a visibilidade da senha."""
        self.show_password = not self.show_password
        if self.show_password:
            self.entry_widget.config(show="")
            
            
            self.toggle_btn.config(text="🔒", fg=colors.get("icon_active_fg", FALLBACK_COLORS["icon_active_fg"]))
        else:
            self.entry_widget.config(show="*")
            
           
            self.toggle_btn.config(text="👁️", fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]))

    def get_value(self):
        """Retorna o valor do campo (limpando o placeholder se presente)."""
        value = self.entry_widget.get()
        return value if value != self.placeholder else ""


# View Principal: SigninView


class SigninView(tk.Frame):
    """Tela de login de usuário"""
    def __init__(self, master, set_session_callback,switch_view_callback=None, root=None, *args, **kwargs):
       
        super().__init__(master, bg=colors["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        
        self.set_session_callback = set_session_callback
        self.switch_view_callback = switch_view_callback
        self.root= root
        self.config(bg=colors["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        

        self.pack_propagate(False)

        self._create_widgets()
        
    def _create_widgets(self):
        # Frame de Conteúdo Principal 
        
        content_frame = tk.Frame(self, bg=colors["bg_main"], padx=30)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.9)
        
        
        tk.Label(content_frame,
                 text="Bem-Vindo de Volta!",
                 font=font_roboto_big,
                 bg=colors["bg_main"],
                 fg=colors["fg_text"]).pack(pady=(10, 5))
        
        
        tk.Label(content_frame,
                 text="É bom vê-lo(a) novamente! Por favor digite suas informações.",
                 font=font_roboto,
                 bg=colors["bg_main"],
                 fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]),
                 wraplength=int(FRAME_WIDTH * 0.8) 
                 ).pack(pady=(0, 25))
        
        # Campos de Entrada
        
        # Campo de Usuário ou E-mail
        self.entry_user_email = CustomEntry(content_frame, "User / E-mail", "Seu nome de usuário ou e-mail")
        self.entry_user_email.pack(fill="x")
        
        # Campo de Senha
        self.entry_password = CustomEntry(content_frame, "Senha", "Sua senha", is_password=True)
        self.entry_password.pack(fill="x")
        
        # 3. Botão de Login 
        login_button = tk.Button(content_frame,
                                 text="Login",
                                 command=self._handle_login,
                                 bg=colors["accent_color"],
                                 fg=colors["fg_text"],
                                 font=font_roboto_big,
                                 height=2,
                                 bd=0,
                                 activebackground=colors.get("accent_color_hover", FALLBACK_COLORS["accent_color_hover"]),
                                 activeforeground=colors["fg_text"],
                                 cursor="hand2")
        login_button.pack(fill="x", pady=(20, 10))
        
        # 4. Rodapé 
        
        footer_frame = tk.Frame(content_frame, bg=colors["bg_main"])
    
        footer_frame.pack(pady=(10, 10))
        
        tk.Label(footer_frame,
                 text="Não tem conta? ",
                 font=font_inter_small,
                 bg=colors["bg_main"],
                 fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"])).pack(side=tk.LEFT)
        
        
        signup_link_text = tk.Button(footer_frame,
                                 text="Cadastre-se",
                                 command=lambda: self._go_to_view("signup"),
                                 font=font_inter_small + ("underline",),
                                 bg=colors["bg_main"],
                                 
                                 fg=colors.get("signup_link_fg", FALLBACK_COLORS["signup_link_fg"]),
                                 bd=0,
                                 activebackground=colors["bg_main"],
                                
                                 activeforeground=colors.get("signup_link_active_fg", FALLBACK_COLORS["signup_link_active_fg"]),
                                 cursor="hand2")
        signup_link_text.pack(side=tk.LEFT)
        
    def _go_to_view(self, view_name):
        """ ação de troca de tela."""
        if self.switch_view_callback:
            
            self.switch_view_callback(view_name)
        else:
            messagebox.showinfo("Navegação Mock", f"Ação de ir para a View: {view_name}")

    def _handle_login(self):
        """Processa a tentativa de login e valida os campos"""
        user_email = self.entry_user_email.get_value()
        password = self.entry_password.get_value()

        # Validação simples
        if not user_email or not password:
            messagebox.showerror("Erro de Login", "Por favor, preencha o usuário/e-mail e a senha.")
            return

        if len(password) < 8:
            messagebox.showerror("Erro de Login", "Senha inválida (simulação: deve ter 8+ caracteres).")
            return
        
        try:
            result = loginController(self.root, user_email, password)
            self.set_session_callback(result)
            
        except Exception as e:
            print("ERRO NO LOGIN:", e)
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro interno", str(e))
            return
        if result != -1 and result != None:  # login bem-sucedido
            messagebox.showinfo("Sucesso", f"Login realizado com sucesso para: {user_email}!")
            self.set_session_callback(result)
            if self.switch_view_callback:

                self.switch_view_callback("home")
        else:
            # Não troca de tela
            return


#Teste de Execução Individual

#
#if __name__ == "__main__":
#    
#    # Config do ambiente de teste com setup_test_window
#    if 'setup_test_window' in locals() and setup_test_window:
#        try:
#            # Garante a definição de cores para o teste antes de inicializar o Tk
#            if "bg_entry" not in colors:
#                 colors["bg_entry"] = FALLBACK_COLORS["bg_entry"]
#            if "fg_secondary" not in colors:
#                 colors["fg_secondary"] = FALLBACK_COLORS["fg_secondary"]
#            if "accent_color_hover" not in colors:
#                 colors["accent_color_hover"] = FALLBACK_COLORS["accent_color_hover"]
#            if "icon_active_fg" not in colors:
#                 colors["icon_active_fg"] = FALLBACK_COLORS["icon_active_fg"]
#            if "signup_link_fg" not in colors:
#                colors["signup_link_fg"] = FALLBACK_COLORS["signup_link_fg"]
#            if "signup_link_active_fg" not in colors:
#                colors["signup_link_active_fg"] = FALLBACK_COLORS["signup_link_active_fg"]
#
#            test_window, root, icones = setup_test_window("Sign In View Teste")
#        except Exception as e:
#            print(f"Erro ao usar setup_test_window: {e}. Usando setup manual.")
#            test_window = None 
#
#    
#    if not 'root' in locals() or not 'test_window' in locals() or test_window is None:
#        # Usa o setup manual 
#        root.title("Sign In View Teste (Manual)")
#        
#        root.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}")
#        
#        test_window = tk.Frame(root)
#        test_window.pack(fill="both", expand=True)
#        icones = {}
#    
#    # Callback mock para a troca de tela
#    def switch_view_mock(view_name):
#        print(f"DEBUG: Tentativa de trocar para a view: {view_name}")
#        for widget in test_window.winfo_children():
#            widget.destroy()
#        
#        tk.Label(test_window,
#                 text=f"Redirecionado para a View: {view_name}",
#                 font=font_roboto_big,
#                 bg=colors["bg_main"],
#                 fg=colors["fg_text"]).pack(pady=FRAME_HEIGHT / 2 - 50)
#        
#    
#    
#    signin_app = SigninView(
#        test_window,
#        switch_view_mock
#    )
#    signin_app.pack(fill="both", expand=True)
#    