APPFILMES
---

## Visão geral

O **APPFILMES** é uma aplicação web em **Python + Flask** que consome a **API do TMDB** para listar e navegar por filmes/séries (populares, em cartaz e categorias), além de expor um endpoint JSON de busca.

## Stack e dependências

- **Backend**: Flask (Blueprints), Jinja2
- **HTTP client**: `requests`
- **Config**: `python-dotenv` (carrega `.env`)
- **UI**: Bootstrap 5 (via CDN)
- **Integração**: The Movie Database (TMDB)

As dependências estão em `requirements.txt`.

## Como rodar (local)

### Pré-requisitos

- **Python 3.11+** (recomendado)
- Uma chave do **TMDB** (API Key) ou **Access Token**

### Setup

Crie e ative um virtualenv (exemplo no Windows PowerShell):

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto (veja `env.example`) e configure suas credenciais do TMDB.

### Executando

```bash
python run.py
```

Por padrão o `run.py` inicializa a app via `create_app()` (em `app/__init__.py`) e executa em **modo debug**.

## Variáveis de ambiente

Configuração utilizada pelo cliente TMDB em `app/api_filmes.py`:

- **TMDB_API_KEY**: API key do TMDB (opcional se usar token)
- **TMDB_ACCESS_TOKEN**: token Bearer do TMDB (opcional se usar api key)
- **TMDB_BASE_URL**: default `https://api.themoviedb.org/3`

> Pelo menos **um** entre `TMDB_API_KEY` ou `TMDB_ACCESS_TOKEN` é obrigatório.

## Rotas (HTTP)

### Páginas (HTML)

- **GET `/`**: home com “Próximas Estreias” (renderiza `app/templates/index.html`)
- **GET `/projeto`**: página “Sobre o Projeto” (renderiza `app/templates/projeto.html`)
- **GET `/filmes/<categoria>`**: listagem por categoria (renderiza `app/templates/filmes.html`)
  - Querystring: `?pagina=1`

Categorias suportadas hoje (mapeadas em `app/routes/filmes.py`):

- `populares`
- `em-cartaz`
- `mais-bem-avaliados`
- `acao`, `comedia`, `drama`, `suspense`, `terror`
- `series-populares`, `series-em-exibicao`, `series-na-tv`, `series-em-breve`

### API (JSON)

- **GET `/api/filmes/buscar?q=<termo>`**: busca por título no TMDB e retorna lista JSON

Exemplo:

```bash
curl "http://127.0.0.1:5000/api/filmes/buscar?q=matrix"
```

## Estrutura do projeto

```
appfilmes/
  app/
    __init__.py            # create_app() + registro de blueprints
    api_filmes.py          # client TMDB (requests) + helpers de imagem
    routes/
      index.py             # rota "/"
      projeto.py           # rota "/projeto"
      filmes.py            # rotas "/filmes/*" + "/api/filmes/buscar"
    templates/
      base.html            # layout (Bootstrap CDN)
      index.html           # home (próximas estreias)
      filmes.html          # listagem por categoria
      projeto.html         # sobre
      components/
        header.html
        footer.html
  run.py                   # entrypoint local (debug=True)
  requirements.txt
```

## Notas técnicas (importante antes de publicar no GitHub)

- **Não versione o virtualenv**: este projeto contém pastas típicas de venv (`Lib/`, `Scripts/`, `pyvenv.cfg`). Para um repositório GitHub, o ideal é remover isso do versionamento e usar `.venv/` localmente.
- **Segredos**: `app/__init__.py` define `SECRET_KEY` hardcoded. Em produção, o recomendado é ler via `.env` (ex.: `FLASK_SECRET_KEY`) e nunca commitar valores reais.
- **Pontos a revisar**:
  - `app/routes/index.py`: quando o TMDB falha (`dados` falso), a rota pode não retornar `render_template` (gera resposta vazia/erro).
  - `app/routes/filmes.py`:
    - há rota de detalhes `'/filmes/<int:filme_id>'` que referencia `detalhes_filme.html`, porém o template não existe atualmente.
    - existe código “morto” após `return jsonify(...)` dentro de `buscar_filmes()` e referência a `em_cartaz.html` (template inexistente).
    - conflito potencial entre `'/filmes/<categoria>'` e `'/filmes/<int:filme_id>'` quando o path é numérico (pode cair na rota de categoria).

## Créditos

- Dados e imagens fornecidos por [TMDB](https://www.themoviedb.org/).
