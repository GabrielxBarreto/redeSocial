import tkinter as tk
from .views.welcome_view import WelcomeView
from .views.signin_view import SigninView
from .views.signup_view import SignupView
from .views.home_feed_view import HomeFeedView
from .views.projects_view import ProjectsView
from .views.create_new_post_view import NovoPostView
from .views.ranking_view import RankingView
from .views.user_profile_view import UserProfileView


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
    elif name == "projects":
        print("entrando na projects")
        current_view = ProjectsView(app_container, switch_view_callback=switch_view)
    elif name == "novoprojeto":
        print("entrando na projects")
        current_view = NovoPostView(app_container, switch_view_callback=switch_view, icones=None)
    elif name == "ranking":
        current_view = RankingView(app_container, switch_view_callback=switch_view, icones=None)
    elif name == "profile":
        mock_user_data = {
        'name': 'Gabriel',
        'username': 'gab_dev',
        'location': 'Chapecó - SC',
        'education': 'UFFS',
        'interests': ['Design', 'Programação', 'Fotografia'],
        'description': 'Apaixonado por tecnologia e design.'
        }
        
        current_view = UserProfileView(
        app_container, 
        user_data=mock_user_data, 
        navigate_back_callback=switch_view  # <-- aqui
)
    else:
        current_view = tk.Label(app_container, text="Tela não encontrada.")

    current_view.pack(fill="both", expand=True)

switch_view("welcome")
root.mainloop()
