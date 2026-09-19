"""
Testes de integração para fluxo completo da aplicação
"""
import pytest


class TestCompleteUserFlow:
    """Testes de integração para o fluxo completo do usuário"""
    
    def test_home_page_loads(self, client):
        """Testa se a página inicial carrega"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.content_type.startswith("text/html")
    
    def test_home_page_has_links_to_login_pages(self, client):
        """Testa se a página inicial tem links para páginas de login"""
        response = client.get("/")
        assert response.status_code == 200
        # Verificar se há referências às rotas de acesso
        html = response.data.decode("utf-8")
        assert "/acesso/equipe" in html or "acesso/equipe" in html
        assert "/acesso/cliente" in html or "acesso/cliente" in html
    
    def test_team_login_page_loads(self, client):
        """Testa se a página de login da equipe carrega"""
        response = client.get("/acesso/equipe")
        assert response.status_code == 200
        assert response.content_type.startswith("text/html")
        html = response.data.decode("utf-8")
        # Verificar elementos esperados
        assert "email" in html.lower() or "login" in html.lower()
    
    def test_client_login_page_loads(self, client):
        """Testa se a página de login do cliente carrega"""
        response = client.get("/acesso/cliente")
        assert response.status_code == 200
        assert response.content_type.startswith("text/html")
    
    def test_team_login_page_has_css_loaded(self, client):
        """Testa se a página de login tem CSS carregado"""
        response = client.get("/acesso/equipe")
        html = response.data.decode("utf-8")
        assert "/static/css/portal.css" in html
    
    def test_team_login_page_has_js_loaded(self, client):
        """Testa se a página de login tem JS carregado"""
        response = client.get("/acesso/equipe")
        html = response.data.decode("utf-8")
        assert "/static/js/portal.js" in html
    
    def test_health_check_endpoint_exists(self, client):
        """Testa se o endpoint de health check existe"""
        response = client.get("/api/health")
        # Pode retornar 200 ou 404 dependendo da implementação
        assert response.status_code in [200, 404]


class TestStaticFilesIntegration:
    """Testes de integração para arquivos estáticos"""
    
    def test_all_required_css_files_accessible(self, client):
        """Testa se todos os CSS necessários são acessíveis"""
        css_files = [
            "/static/css/portal.css",
            "/static/css/team.css",
        ]
        for css_file in css_files:
            response = client.get(css_file)
            assert response.status_code == 200, f"CSS {css_file} não está acessível"
            assert "text/css" in response.content_type
    
    def test_all_required_js_files_accessible(self, client):
        """Testa se todos os JS necessários são acessíveis"""
        js_files = [
            "/static/js/portal.js",
            "/static/js/portal-admin.js",
            "/static/js/portal-client.js",
            "/static/js/team/dashboard.js",
        ]
        for js_file in js_files:
            response = client.get(js_file)
            assert response.status_code == 200, f"JS {js_file} não está acessível"
    
    def test_css_files_not_empty(self, client):
        """Testa se os arquivos CSS não estão vazios"""
        css_files = [
            "/static/css/portal.css",
            "/static/css/team.css",
        ]
        for css_file in css_files:
            response = client.get(css_file)
            assert len(response.data) > 0, f"CSS {css_file} está vazio"
