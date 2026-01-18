# importar create_app do arquivo app/__init__.py
from app import create_app

# criar a aplicação Flask
app = create_app()

# se o arquivo for executado diretamente, rodar a aplicação em modo de desenvolvimento
if __name__ == '__main__':
    # rodar a aplicação em modo de desenvolvimento
    app.run(debug=True)