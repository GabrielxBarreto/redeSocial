from .views.create_new_post_view  import *
from .views.home_feed_view import *
if __name__ == "__main__":


    test_window, root, icones_mock = setup_test_window("Teste Individual: Novo Post") 
    
    # Passa os ícones carregados para a função de criação da aba
    frame = criar_aba_novo_post(test_window, icones_mock)
    frame.pack(fill="both", expand=True)
    
    root.mainloop()


   # Usa a função de setup do utils_icons para inicializar a janela
    test_window, root, icones = setup_test_window("Home View Teste")
    
    if test_window:
        # Frame container para simular o corpo do aplicativo
        app_body = tk.Frame(test_window, bg=colors.bg_main if hasattr(colors, 'bg_main') else colors["bg_main"])
        app_body.pack(fill="both", expand=True)

        # Função de callback de mock para a navegação
        def mock_switch_view(view_name):
            print(f"Navegação Mock: Trocando para {view_name}")

        # Cria e exibe a view de Home
        home_frame = HomeView(app_body, mock_switch_view, icones)
        home_frame.pack(fill="both", expand=True)

        # Mocka a BottomBar para garantir que o GC não colete os PhotoImages
        try:
            from utils_icons import BottomBar # Importa a barra inferior para o teste
            current_view_state = tk.StringVar(value="Home")
            
            # Cria a barra, embora não seja usada para navegação real no teste, 
            # garante que as dependências do PhotoImage sejam resolvidas.
            bottom_bar_frame = BottomBar(test_window, mock_switch_view, icones, current_view_state)
            bottom_bar_frame.pack(fill="x", side=tk.BOTTOM)
        except ImportError:
            print("BottomBar não pôde ser importada para o teste. Apenas a HomeView será exibida.")
            
        test_window.mainloop()
        # Após fechar o Toplevel, certifique-se de fechar a raiz
        try:
            root.destroy()
        except:
            pass
    else:
        print("Falha na inicialização da janela de teste. Verifique as dependências.")
    