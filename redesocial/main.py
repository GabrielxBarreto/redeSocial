import tkinter as tk
from .views.welcome_view import WelcomeView
from .views.signin_view import SigninView

root = tk.Tk()
root.geometry("400x600")

current_view = None

def switch_view(view_name):
    global current_view

    # remove a view atual
    if current_view:
        current_view.destroy()

    # cria a próxima
    if view_name == "welcome":
        current_view = WelcomeView(root, switch_view)
    elif view_name == "signin":
        current_view = SigninView(root, switch_view)
    else:
        current_view = tk.Label(root, text="TBD...")

    current_view.pack(fill="both", expand=True)

# cria as telas
welcome_frame = WelcomeView(root, switch_view)
login_frame = SigninView(root, switch_view)

# começa mostrando a welcome
welcome_frame.pack(fill="both", expand=True)

root.mainloop()
