
from .views.welcome_view import *
from .views.signin_view import *

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Welcome View Teste")
    root.geometry(f"{FALLBACK_WIDTH}x{FALLBACK_HEIGHT}")
    
    test_frame = tk.Frame(root)
    test_frame.pack(fill="both", expand=True)
    
    def switch_view(view_name):
        messagebox.showinfo("Navegação", f"Navegar para a View: {view_name}")
    
    welcome_app = WelcomeView(
        test_frame,
        switch_view
    )
    welcome_app.pack(fill="both", expand=True)
    
    root.mainloop()
   