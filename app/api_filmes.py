import os
import requests
from functools import lru_cache
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class TMDBClient:
    """Cliente para integração com a API do TMDB"""
    
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.access_token = os.getenv('TMDB_ACCESS_TOKEN')
        self.base_url = os.getenv('TMDB_BASE_URL', 'https://api.themoviedb.org/3')
        self.image_base_url = 'https://image.tmdb.org/t/p/w500'
        
        if not self.api_key and not self.access_token:
            raise ValueError("TMDB_API_KEY ou TMDB_ACCESS_TOKEN deve estar configurado")
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers para autenticação"""
        if self.access_token:
            return {'Authorization': f'Bearer {self.access_token}'}
        return {}
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Faz requisição para a API do TMDB"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        request_params = params or {}
        if self.api_key:
            request_params['api_key'] = self.api_key
        
        try:
            response = requests.get(url, headers=headers, params=request_params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição TMDB: {e}")
            return None
    
    def buscar_filmes_populares(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes populares"""
        return self._make_request('/movie/popular', {'page': pagina, 'language': idioma})
    
    def buscar_filmes_por_acao(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes por ação"""
        return self._make_request('/discover/movie', {'page': pagina, 'language': idioma, 'with_genres': '28'})
    
    def buscar_filmes_por_comedia(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes por comédia"""
        return self._make_request('/discover/movie', {'page': pagina, 'language': idioma, 'with_genres': '35'})
    
    def buscar_filmes_por_drama(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes por drama"""
        return self._make_request('/discover/movie', {'page': pagina, 'language': idioma, 'with_genres': '18'})
    
    def buscar_filmes_por_suspense(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes por suspense"""
        return self._make_request('/discover/movie', {'page': pagina, 'language': idioma, 'with_genres': '53'})
    
    def buscar_filmes_por_terror(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes por terror"""
        return self._make_request('/discover/movie', {'page': pagina, 'language': idioma, 'with_genres': '27'})
    
    def buscar_filme_por_id(self, filme_id: int, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca detalhes de um filme específico"""
        return self._make_request(f'/movie/{filme_id}', {'language': idioma})
    
    def buscar_filmes_por_titulo(self, titulo: str, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes por título"""
        return self._make_request('/search/movie', {
            'query': titulo,
            'page': pagina,
            'language': idioma
        })
    
    def buscar_proximas_estreias(self, pagina: int = 1, idioma: str = 'pt-BR', data_inicio: str = '2026-01-01', data_fim: str = '2026-12-31') -> Optional[Dict]:
        """Busca filmes em cartaz nos cinemas"""
        return self._make_request('/movie/upcoming', {'page': pagina, 'language': idioma, 'start_date': data_inicio, 'end_date': data_fim})
    
    def buscar_filmes_em_cartaz(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes em cartaz nos cinemas"""
        return self._make_request('/movie/now_playing', {'page': pagina, 'language': idioma})
    
    def buscar_series_populares(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca séries populares"""
        return self._make_request('/tv/popular', {'page': pagina, 'language': idioma})
    
    def buscar_series_na_tv(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca séries na TV"""
        return self._make_request('/tv/airing_today', {'page': pagina, 'language': idioma})
    
    def buscar_series_em_exibicao(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca séries em exibição"""
        return self._make_request('/tv/on_the_air', {'page': pagina, 'language': idioma})
    
    def buscar_filmes_mais_bem_avaliados(self, pagina: int = 1, idioma: str = 'pt-BR') -> Optional[Dict]:
        """Busca filmes mais bem avaliados (top rated)"""
        return self._make_request('/movie/top_rated', {'page': pagina, 'language': idioma})
    
    def obter_url_imagem(self, caminho: str) -> str:
        """Retorna URL completa da imagem"""
        if not caminho:
            return ''
        return f"{self.image_base_url}{caminho}"

# Instância global do cliente
_client = None

def get_tmdb_client() -> TMDBClient:
    """Retorna instância singleton do cliente TMDB"""
    global _client
    if _client is None:
        _client = TMDBClient()
    return _client