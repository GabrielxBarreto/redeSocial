import tkinter as tk
from .views.welcome_view import WelcomeView
from .views.signin_view import SigninView
from .views.signup_view import SignupView
from .views.home_feed_view import HomeFeedView

root = tk.Tk()
root.geometry("400x600")

# container fixo
app_container = tk.Frame(root)
app_container.pack(fill="both", expand=True)

current_view = None

def switch_view(name):
    global current_view

    # limpa apenas o container, não o root
    for widget in app_container.winfo_children():
        widget.destroy()

    if name == "welcome":
        current_view = WelcomeView(app_container, switch_view_callback=switch_view)
    elif name == "signin":
        current_view = SigninView(app_container, switch_view_callback=switch_view)
    elif name == "signup":
        current_view = SignupView(app_container, switch_view_callback=switch_view)
    elif name == "home":
        print("entrando na home")
        current_view = HomeFeedView(app_container, switch_view_callback=switch_view)
    else:
        current_view = tk.Label(app_container, text="Tela não encontrada.")

    current_view.pack(fill="both", expand=True)

switch_view("welcome")
root.mainloop()
