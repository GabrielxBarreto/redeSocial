import tkinter as tk
from tkinter import messagebox
import sys
from  ..controller.authController import signupController

# 1. Definições de Cores e Fontes AUTONOMO

# Defs de Cores
colors = {
    "bg_main": "#1A1A1A",               # Fundo Principal Escuro
    "fg_text": "#ffffff",               # Cor do Texto Claro
    "accent_color": "#6F42C1",          # Roxo do Botão Principal
    "accent_color_hover": "#5A369A",    # Roxo do Botão (Hover)
    "bg_entry": "#3C3C3C",              # Fundo dos Campos de Entrada
    "bg_entry_border": "#3C3C3C",       # Borda/Container dos Campos
    "fg_secondary": "#aaaaaa",          # Texto Secundário (Placeholders)
    "icon_active_fg": "#ffffff",        # Cor do Ícone Ativo
}

# Defs de Fontes e Dimensões
font_roboto_big = ("Roboto", 16, "bold")
font_roboto = ("Roboto", 12)
font_entry = ("Roboto", 14) 
font_inter_small = ("Inter", 10)
FRAME_WIDTH, FRAME_HEIGHT = 400, 600
FALLBACK_ENTRY_BORDER_COLOR = colors.get("accent_color", colors["accent_color"]) 




class CustomEntry(tk.Frame):
    """
    Frame customizado que envolve um Label e um Entry para um visual limpo e moderno.
    Inclui lógica de placeholder e toggle de visibilidade de senha.
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

        # Container para a borda visual
        entry_container = tk.Frame(self, bg=self.entry_border_color, height=50) 
        entry_container.pack(fill="x", ipady=3, pady=(0, 15))
        entry_container.pack_propagate(False) 

        # Campo de Entrada 
        self.entry_widget = tk.Entry(entry_container,
                                     textvariable=self.var,
                                     font=font_entry,
                                     bg=colors.get("bg_entry"),
                                     fg=colors["fg_text"],
                                     insertbackground=colors["fg_text"], 
                                     bd=0, 
                                     highlightthickness=0) 
        
        entry_y_padding = 5 
        
        # Config de Senha
        if self.is_password:
            self.entry_widget.config(show="*" if not self.show_password else "")
        
        # Config inicial do Placeholder
        self.entry_widget.insert(0, self.placeholder)
        self.entry_widget.config(fg=colors.get("fg_secondary"))
        
        
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
            self.entry_widget.config(fg=colors.get("fg_secondary"))
            
            
            if self.is_password:
                self.entry_widget.config(show="")

    def _create_password_toggle_button(self, master):
        """Cria o botão de mostrar/esconder senha."""
        self.toggle_btn = tk.Label(master, 
                                   text="👁️", 
                                   font=("Arial", 14), 
                                   bg=colors.get("bg_entry"), 
                                   fg=colors.get("fg_secondary"),
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
            self.toggle_btn.config(text="👁️", fg=colors.get("fg_secondary"))

    def get_value(self):
        """Retorna o valor do campo (limpando o placeholder se presente)."""
        value = self.entry_widget.get()
       
        return value if value != self.placeholder else ""




#  View Principal: SignupView com Scrollbar

class SignupView(tk.Frame):
    """Tela de cadastro de novo usuário com suporte a rolagem (Scrollbar)."""
    def __init__(self, master, switch_view_callback=None, icones=None, *args, **kwargs):
        super().__init__(master)
        self.switch_view_callback = switch_view_callback
        self.icones = icones if icones else {} 
        
        self.config(bg=colors["bg_main"], width=FRAME_WIDTH, height=FRAME_HEIGHT)
        
        self.pack_propagate(False)

        self._create_scrollable_widgets()
        
    def _create_scrollable_widgets(self):
        """Configura o Canvas e o Frame interno para permitir rolagem."""
        
        #  Canvas para Rolagem
        self.canvas = tk.Canvas(self, bg=colors["bg_main"], highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Config do Canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        #  Frame de Conteúdo 
        self.scrollable_frame = tk.Frame(self.canvas, bg=colors["bg_main"], padx=30, pady=20)
        
        # Adiciona o Frame de Conteúdo ao Canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Binds para atualizar a área de rolagem
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
    
        self.canvas.bind(
            '<Configure>',
            lambda e: self.canvas.itemconfig(
                self.canvas.find_withtag("all")[0], 
                width=e.width
            )
        )
        
       
        self._create_form_widgets(self.scrollable_frame)
        
    def _create_form_widgets(self, container_frame):
        # Frame de Conteúdo Principal
        
        # Header 
        header_frame = tk.Frame(container_frame, bg=colors["bg_main"])
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Botão de Voltar
        back_button = tk.Button(header_frame, 
                                command=self._go_back,
                                bd=0, 
                                bg=colors["bg_main"],
                                fg=colors["fg_text"],
                                font=font_roboto_big,
                                text="<", 
                                activebackground=colors["bg_main"],
                                activeforeground=colors.get("fg_secondary"), 
                                cursor="hand2")
        
        if self.icones.get("back_icon"):
            back_button.config(image=self.icones["back_icon"], text="")
            back_button.image = self.icones["back_icon"] 
        
        back_button.pack(side=tk.LEFT, anchor="w")

        # Título da Tela
        tk.Label(header_frame, 
                 text="Crie sua conta", 
                 font=font_roboto_big, 
                 bg=colors["bg_main"], 
                 fg=colors["fg_text"]).pack(side=tk.LEFT, padx=(10, 0), anchor="w")
        
        #  Campos de Entrada 

        form_frame = container_frame 

        # Campos individuais 
        self.entry_user = CustomEntry(form_frame, "User", "Seu nome de usuário")
        self.entry_user.pack(fill="x")
        
        self.entry_password = CustomEntry(form_frame, "Senha", "Mínimo 8 caracteres", is_password=True)
        self.entry_password.pack(fill="x")

        self.entry_email = CustomEntry(form_frame, "E-mail", "nome@exemplo.com")
        self.entry_email.pack(fill="x")
        
        # Campo de Agrupamento para Nascimento
        tk.Label(form_frame,
                 text="Data de Nascimento",
                 font=font_roboto,
                 bg=colors["bg_main"],
                 fg=colors["fg_text"],
                 anchor="w").pack(fill="x", pady=(5, 2))


        # Campos de Data de Nascimento
        date_frame = tk.Frame(form_frame, bg=colors["bg_main"])
        date_frame.pack(fill="x", pady=(5, 10))

        self.entry_day = CustomEntry(date_frame, "Dia", "DD")
        self.entry_month = CustomEntry(date_frame, "Mês", "MM")
        self.entry_year = CustomEntry(date_frame, "Ano", "AAAA")

        
        self.entry_day.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        self.entry_month.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        self.entry_year.pack(side=tk.LEFT, fill="x", expand=True)
        self.entry_gender = CustomEntry(form_frame, "Gênero", "Digite seu gênero")
        self.entry_gender.pack(fill="x")
        
        
        # Botão de Cadastro 
        register_button = tk.Button(form_frame, 
                                    text="Criar Conta", 
                                    command=self._handle_signup,
                                    bg=colors["accent_color"],
                                    fg=colors["fg_text"],
                                    font=font_roboto_big,
                                    height=2,
                                    bd=0,
                                    activebackground=colors.get("accent_color_hover"),
                                    activeforeground=colors["fg_text"],
                                    cursor="hand2")
        register_button.pack(fill="x", pady=(20, 10))
        
        # 4. Mensagem de rodapé
        tk.Label(form_frame, 
                 text="Ao se cadastrar, você concorda com nossos termos.", 
                 font=font_inter_small, 
                 bg=colors["bg_main"], 
                 fg=colors.get("fg_secondary")).pack(pady=(5, 0))

    def _go_back(self):
        """Simula a ação de voltar, ou chama o callback se fornecido."""
        self.switch_view_callback("signin") 

    def _handle_signup(self):
        """Processa a tentativa de cadastro e valida os campos."""
        user = self.entry_user.get_value()
        print(type(user))
        password = self.entry_password.get_value()
        email = self.entry_email.get_value()
        day = self.entry_day.get_value()
        month = self.entry_month.get_value()
        year = self.entry_year.get_value()
        gender = self.entry_gender.get_value() 

        # Validação de campos obrigatórios
        if not user or not password or not email or not day or not month or not year:
            messagebox.showerror("Erro de Cadastro", "Por favor, preencha todos os campos obrigatórios.")
            return

        if len(password) < 8:
            messagebox.showerror("Erro de Cadastro", "A senha deve ter no mínimo 8 caracteres.")
            return
            
        if "@" not in email or "." not in email:
            messagebox.showerror("Erro de Cadastro", "E-mail inválido.")
            return

        # Tentativa de converter data para números
        try:
            int(day), int(month), int(year)
        except ValueError:
            messagebox.showerror("Erro de Data", "A data de nascimento deve conter apenas números.")
            return
        signupController(self.master,user,email,password,day,month,year,gender)
        
        # Em uma aplicação real, o usuário seria redirecionado para o Home Feed
        if self.switch_view_callback:
            self.switch_view_callback("home")


#  Teste de Execução Individual

if __name__ == "__main__":
    
    # Config Manual do Ambiente de Teste
    root = tk.Tk()
    root.title("Sign Up View Teste")
    
    root.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}")
    root.configure(bg=colors["bg_main"])
    
    # Frame que irá conter a SignupView
    test_window = tk.Frame(root, bg=colors["bg_main"])
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