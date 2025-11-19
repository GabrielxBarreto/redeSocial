# Rede Social para Cientistas da Computação

Uma rede social voltada para cientistas da computação, desenvolvida para troca de conhecimento, compartilhamento de projetos, artigos, tutoriais e discussões técnicas, utilizando **Python**, **Tkinter** e **Pandas**.  

## Funcionalidades

- Cadastro e autenticação de usuários
- Criação e interação com publicações (posts, comentários, curtidas)
- Perfis com informações técnicas e áreas de interesse
- Feed personalizado de acordo com interesses do usuário
- Manipulação e análise de dados com **Pandas**  
- Interface gráfica intuitiva com **Tkinter**
- Armazenamento de dados local em arquivos CSV

## Tecnologias

- **Python 3.11+**
- **Tkinter** (interface gráfica)
- **Pandas** (manipulação e análise de dados)
- Sistema de virtualenv para isolamento do ambiente

## Pré-requisitos (Linux)

- Python 3 instalado
- pip instalado

## Instalação

1. Clone o repositório (ou baixe o ZIP):

```bash
git clone https://github.com/seuusuario/redesocial.git
cd redesocial

    Crie um ambiente virtual:

python3 -m venv venv

    Ative o ambiente virtual:

source venv/bin/activate

    Instale as dependências:

pip install -r requirements.txt

    Certifique-se de que o Tkinter esteja instalado no seu Linux. Em distribuições Debian/Ubuntu, você pode instalar com:

sudo apt-get install python3-tk
