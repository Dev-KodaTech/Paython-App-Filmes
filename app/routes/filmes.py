from flask import Blueprint, render_template, request, jsonify
from app.api_filmes import get_tmdb_client

filmes_bp = Blueprint('filmes', __name__)
    
# Rota para buscar por categoria
@filmes_bp.route("/filmes/<categoria>")
def filmes_categoria(categoria):
    categoria = categoria.lower().strip()
    pagina = request.args.get("pagina", 1, type=int)

    MAP = {
        "populares": "buscar_filmes_populares",
        "em-cartaz": "buscar_filmes_em_cartaz",
        "mais-bem-avaliados": "buscar_filmes_mais_bem_avaliados",
        "acao": "buscar_filmes_por_acao",
        "comedia": "buscar_filmes_por_comedia",
        "drama": "buscar_filmes_por_drama",
        "suspense": "buscar_filmes_por_suspense",
        "terror": "buscar_filmes_por_terror",
        "series-populares": "buscar_series_populares",
        "series-em-exibicao": "buscar_series_em_exibicao",
        "series-na-tv": "buscar_series_na_tv",
        "series-em-breve": "buscar_series_em_breve"
    }

    if categoria not in MAP:
        return "Categoria não encontrada", 404

    tmdb = get_tmdb_client()
    metodo = getattr(tmdb, MAP[categoria])
    dados = metodo(pagina=pagina)

    filmes = (dados or {}).get("results", [])
    return render_template("filmes.html", filmes=filmes, categoria=categoria)

    
# Rota para buscar filme por ID
@filmes_bp.route('/filmes/<int:filme_id>')
def detalhes_filme(filme_id):
    tmdb = get_tmdb_client()
    filme = tmdb.buscar_filme_por_id(filme_id)
    
    if not filme:
        return "Filme não encontrado", 404
    
    filme['poster_url'] = tmdb.obter_url_imagem(filme.get('poster_path'))
    filme['backdrop_url'] = tmdb.obter_url_imagem(filme.get('backdrop_path'))
    
    return render_template('detalhes_filme.html', filme=filme)

# Rota para buscar filmes por título
@filmes_bp.route('/api/filmes/buscar')
def buscar_filmes():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Parâmetro q é obrigatório'}), 400
    
    tmdb = get_tmdb_client()
    dados = tmdb.buscar_filmes_por_titulo(query)
    
    if not dados:
        return jsonify({'error': 'Erro ao buscar filmes'}), 500
    
    filmes = dados.get('results', [])
    for filme in filmes:
        filme['poster_url'] = tmdb.obter_url_imagem(filme.get('poster_path'))
    
    return jsonify(filmes)
  
    tmdb = get_tmdb_client()
    pagina = request.args.get('pagina', 1, type=int)
    dados = tmdb.buscar_filmes_em_cartaz(pagina=pagina)
    
    if not dados:
        filmes_lista = []
    else:
        filmes_lista = dados.get('results', [])
        # Adicionar URL completa das imagens
        for filme in filmes_lista:
            filme['poster_url'] = tmdb.obter_url_imagem(filme.get('poster_path'))
            filme['backdrop_url'] = tmdb.obter_url_imagem(filme.get('backdrop_path'))
    
    return render_template('em_cartaz.html', filmes=filmes_lista)
  
  