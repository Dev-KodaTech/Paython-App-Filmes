from flask import Blueprint, render_template, request
from app.api_filmes import get_tmdb_client

# Criar um blueprint para as rotas da index
index_bp = Blueprint("index", __name__)

"""
# Criar uma rota para a index
@index_bp.route("/")
def index():
    return render_template("index.html")
"""

# Rota para buscar Proximas Estreias
@index_bp.route('/')
def proximas_estreias():
    tmdb = get_tmdb_client()
    pagina = request.args.get('pagina', 1, type=int)
    dados = tmdb.buscar_proximas_estreias(pagina=pagina)
    if not dados:
        filmes_estreias_lista = []
    else:
        filmes_estreias_lista = dados.get('results', [])[:8]
        # Adicionar URL completa das imagens
        for filme in filmes_estreias_lista:
            filme['poster_url'] = tmdb.obter_url_imagem(filme.get('poster_path'))
            filme['backdrop_url'] = tmdb.obter_url_imagem(filme.get('backdrop_path'))
        return render_template('index.html', filmes=filmes_estreias_lista)