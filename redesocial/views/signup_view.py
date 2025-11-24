import tkinter as tk
from tkinter import messagebox
import sys


# 1. Defs de Fallback 



FALLBACK_COLORS = {
    "bg_main": "#1A1A1A",            
    "fg_text": "#ffffff",
    "accent_color": "#6F42C1",       # Roxo Botão
    "accent_color_hover": "#5A369A", 
    "bg_entry": "#3C3C3C",           
    "bg_entry_border": "#3C3C3C",    
    "fg_secondary": "#aaaaaa",
    "icon_active_fg": "#ffffff",
}
# --- Fim das alterações de cor ---

FALLBACK_FONT_BIG = ("Roboto", 16, "bold")
FALLBACK_FONT_DEFAULT = ("Roboto", 12)
FALLBACK_FONT_ENTRY = ("Roboto", 14) 
FALLBACK_FONT_SMALL = ("Inter", 10)
FALLBACK_WIDTH, FALLBACK_HEIGHT = 400, 600

# Tenta importar do utils_icons, definindo fallbacks se a importação falhar
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
    
    font_entry = ("Roboto", 14)
    
    # Se importado, sobrescreve as cores do utils_icons
    colors.update(FALLBACK_COLORS)

except ImportError:
    # Se o utils_icons falhar completamente, usamos os fallbacks
    print("Aviso: Falha ao importar utils_icons.py. Usando cores e fontes padrão.")
    colors = FALLBACK_COLORS
    font_roboto_big = FALLBACK_FONT_BIG
    font_roboto = FALLBACK_FONT_DEFAULT
    font_entry = FALLBACK_FONT_ENTRY 
    font_inter_small = FALLBACK_FONT_SMALL
    FRAME_WIDTH = FALLBACK_WIDTH
    FRAME_HEIGHT = FALLBACK_HEIGHT
    setup_test_window = None 

# Garante que a cor de borda exista 
FALLBACK_ENTRY_BORDER_COLOR = colors.get("accent_color", FALLBACK_COLORS["accent_color"]) 



# 2. Componente customizado para o Campo de Entrada


class CustomEntry(tk.Frame):
    """
    Frame customizado que envolve um Label e um Entry para um visual limpo e moderno.
    """
    def __init__(self, master, label_text, placeholder="", is_password=False, **kwargs):
        super().__init__(master, bg=colors["bg_main"], **kwargs)
        self.label_text = label_text
        self.placeholder = placeholder
        self.is_password = is_password
        self.show_password = not is_password
        self.var = tk.StringVar()
        
        
        self.entry_border_color = colors["bg_entry_border"] 

        self._create_widgets()

    def _create_widgets(self):
       
        tk.Label(self, 
                 text=self.label_text, 
                 font=font_roboto, 
                 bg=colors["bg_main"], 
                 fg=colors["fg_text"],
                 anchor="w").pack(fill="x", pady=(5, 2))

       
        entry_container = tk.Frame(self, bg=self.entry_border_color, height=50) 
        entry_container.pack(fill="x", ipady=3, pady=(0, 15))
        entry_container.pack_propagate(False) 

        # Campo de Entrada 
        self.entry_widget = tk.Entry(entry_container,
                                     textvariable=self.var,
                                     font=font_entry,
                                     bg=colors.get("bg_entry", FALLBACK_COLORS["bg_entry"]),
                                     fg=colors["fg_text"],
                                     insertbackground=colors["fg_text"], 
                                     bd=0, 
                                     highlightthickness=0) 
        
        entry_y_padding = 5 
        
        
        if self.is_password:
            self.entry_widget.config(show="*" if not self.show_password else "")
        
        
        self.entry_widget.insert(0, self.placeholder)
        
       
        self.entry_widget.config(fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]))
        
        self.entry_widget.bind("<FocusIn>", self._clear_placeholder)
        self.entry_widget.bind("<FocusOut>", self._restore_placeholder)
        
        
        entry_xpad = 5
        if self.is_password:
           
            self.entry_widget.pack(side=tk.LEFT, fill="x", expand=True, padx=(entry_xpad, 0), pady=entry_y_padding)
            self._create_password_toggle_button(entry_container)
        else:
            
            self.entry_widget.pack(side=tk.LEFT, fill="x", expand=True, padx=(entry_xpad, 5), pady=entry_y_padding)

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
                                   bg=colors.get("bg_entry", FALLBACK_COLORS["bg_entry"]), 
                                   fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]),
                                   cursor="hand2")
        self.toggle_btn.bind("<Button-1>", self._toggle_password_visibility)
        self.toggle_btn.pack(side=tk.RIGHT, padx=5, pady=5) 

    def _toggle_password_visibility(self, event):
        """Alterna a visibilidade da senha."""
        self.show_password = not self.show_password
        if self.show_password:
            self.entry_widget.config(show="")
            
            self.toggle_btn.config(text="🔒", fg=colors.get("icon_active_fg", colors["fg_text"]))
        else:
            self.entry_widget.config(show="*")
            
            self.toggle_btn.config(text="👁️", fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"]))

    def get_value(self):
        """Retorna o valor do campo (limpando o placeholder se presente)."""
        value = self.entry_widget.get()
        return value if value != self.placeholder else ""


# 3. View Principal: SignupView


class SignupView(tk.Frame):
    """Tela de cadastro de novo usuário."""
    def __init__(self, master, switch_view_callback=None, icones=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.switch_view_callback = switch_view_callback
        self.icones = icones if icones else {} 
        
        self.config(bg=colors["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.pack_propagate(False)

        self._create_widgets()
        
    def _create_widgets(self):
        # Frame de Conteúdo Principal
        
        content_frame = tk.Frame(self, bg=colors["bg_main"], padx=30, pady=20)
        content_frame.pack(fill="both", expand=True) 

        # 1. Header 
        header_frame = tk.Frame(content_frame, bg=colors["bg_main"])
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Botão de Voltar
        back_button = tk.Button(header_frame, 
                                 text="<", 
                                 command=self._go_back,
                                 bd=0, 
                                 bg=colors["bg_main"],
                                 fg=colors["fg_text"],
                                 font=font_roboto_big,
                                 activebackground=colors["bg_main"],
                                
                                 activeforeground=colors.get("fg_secondary", colors["fg_text"]), 
                                 cursor="hand2")
        
        if self.icones.get("back_icon"):
            back_button.config(image=self.icones["back_icon"], text="")
            back_button.image = self.icones["back_icon"] 
        
        back_button.pack(side=tk.LEFT, anchor="w")

        
        tk.Label(header_frame, 
                 text="Crie sua conta", 
                 font=font_roboto_big, 
                 bg=colors["bg_main"], 
                 fg=colors["fg_text"]).pack(side=tk.LEFT, padx=(10, 0), anchor="w")
        
        # 2. Campos de Entrada 

        form_frame = content_frame 

        # Campos individuais 
        self.entry_user = CustomEntry(form_frame, "User", "Seu nome de usuário")
        self.entry_user.pack(fill="x")
        
        self.entry_password = CustomEntry(form_frame, "Senha", "Mínimo 8 caracteres", is_password=True)
        self.entry_password.pack(fill="x")

        self.entry_email = CustomEntry(form_frame, "E-mail", "nome@exemplo.com")
        self.entry_email.pack(fill="x")
        
        
        tk.Label(form_frame,
                 text="Nascimento",
                 font=font_roboto,
                 bg=colors["bg_main"],
                 fg=colors["fg_text"],
                 anchor="w").pack(fill="x", pady=(5, 2))


        # Campos de Data de Nascimento 
        date_frame = tk.Frame(form_frame, bg=colors["bg_main"])
        date_frame.pack(fill="x", pady=(5, 10))

        # Títulos dos campos de data
        self.entry_day = CustomEntry(date_frame, "Dia", "DD")
        self.entry_month = CustomEntry(date_frame, "Mês", "MM")
        self.entry_year = CustomEntry(date_frame, "Ano", "AAAA")

        
        self.entry_day.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        self.entry_month.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        self.entry_year.pack(side=tk.LEFT, fill="x", expand=True)

        # Botão de Cadastro 
        register_button = tk.Button(form_frame, 
                                     text="Criar Conta", 
                                     command=self._handle_signup,
                                     bg=colors["accent_color"],
                                     fg=colors["fg_text"],
                                     font=font_roboto_big,
                                     height=2,
                                     bd=0,
                                     activebackground=colors.get("accent_color_hover", colors["accent_color"]),
                                     activeforeground=colors["fg_text"],
                                     cursor="hand2")
        register_button.pack(fill="x", pady=(20, 10))
        
        # 4. Mensagem de rodapé
        tk.Label(form_frame, 
                 text="Ao se cadastrar, você concorda com nossos termos.", 
                 font=font_inter_small, 
                 bg=colors["bg_main"], 
                 fg=colors.get("fg_secondary", FALLBACK_COLORS["fg_secondary"])).pack(pady=(5, 0))

    def _go_back(self):
        """Simula a ação de voltar, ou chama o callback se fornecido."""
        if self.switch_view_callback:
            self.switch_view_callback("SignIn") 
        else:
            messagebox.showinfo("Navegação Mock", "Ação de Voltar (SignIn View) - Faria a troca de tela.")

    def _handle_signup(self):
        """Processa a tentativa de cadastro e valida os campos."""
        user = self.entry_user.get_value()
        password = self.entry_password.get_value()
        email = self.entry_email.get_value()
        day = self.entry_day.get_value()
        month = self.entry_month.get_value()
        year = self.entry_year.get_value()

        # Validação simples
        if not user or not password or not email or not day or not month or not year:
            messagebox.showerror("Erro de Cadastro", "Por favor, preencha todos os campos.")
            return

        if len(password) < 8:
            messagebox.showerror("Erro de Cadastro", "A senha deve ter no mínimo 8 caracteres.")
            return
            
        if "@" not in email or "." not in email:
            messagebox.showerror("Erro de Cadastro", "E-mail inválido.")
            return

      
        messagebox.showinfo("Sucesso", f"Conta criada para o usuário: {user}!")
        
        # Em uma aplicação real, o usuário seria redirecionado para o Home Feed
        if self.switch_view_callback:
            self.switch_view_callback("Home")



# 4. Teste de Execução Individual


if __name__ == "__main__":
    
    # 1. Configuração do ambiente de teste com setup_test_window
    if setup_test_window:
        try:
            test_window, root, icones = setup_test_window("Sign Up View Teste")
        except Exception as e:
            
            print(f"Erro ao usar setup_test_window: {e}. Usando setup manual.")
            test_window = None # Flag para setup manual

    # Configuração Manual
    if not setup_test_window or not 'root' in locals():
        
        root = tk.Tk()
        root.title("Sign Up View Teste (Manual)")
        
        root.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}")
        
        test_window = tk.Frame(root)
        test_window.pack(fill="both", expand=True)
        icones = {}
    
    # Callback mock para a troca de tela
    def switch_view_mock(view_name):
        print(f"DEBUG: Tentativa de trocar para a view: {view_name}")
        for widget in test_window.winfo_children():
            widget.destroy()
        
        tk.Label(test_window, 
                 text=f"Redirecionado para a View: {view_name}", 
                 font=font_roboto_big, 
                 bg=colors["bg_main"], 
                 fg=colors["fg_text"]).pack(pady=FRAME_HEIGHT / 2 - 50)
        
    

    signup_app = SignupView(
        test_window, 
        switch_view_mock, 
        icones
    )
    signup_app.pack(fill="both", expand=True)
    
    
    root.mainloop()