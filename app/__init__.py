# Importar Flask e criar uma instância do Flask
from flask import Flask
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Importar todas as rotas
from app.routes import index_bp, projeto_bp, filmes_bp

# Criar a aplicação Flask
def create_app():
    app = Flask(__name__)
    
    # Configuração da aplicação
    app.config["SECRET_KEY"] = "any-random-secret-key"
    
    # Importar todas as rotas
    app.register_blueprint(index_bp)
    app.register_blueprint(projeto_bp)
    app.register_blueprint(filmes_bp)
    

    return app