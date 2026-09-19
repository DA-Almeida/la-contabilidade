"""
Testes para rotas públicas (sem autenticação)
"""
import pytest


class TestPublicRoutes:
    """Testes para rotas públicas"""
    
    def test_home_route_returns_200(self, client):
        """Testa se a rota / retorna status 200"""
        response = client.get("/")
        assert response.status_code == 200
        assert b"<!doctype html>" in response.data or b"<!DOCTYPE html>" in response.data
    
    def test_home_route_returns_html(self, client):
        """Testa se a rota / retorna HTML"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.content_type.startswith("text/html")
    
    def test_team_access_route_without_html_extension(self, client):
        """Testa se /acesso/equipe existe (sem .html)"""
        response = client.get("/acesso/equipe")
        assert response.status_code == 200
        assert response.content_type.startswith("text/html")
    
    def test_team_access_returns_portal_admin_html(self, client):
        """Testa se /acesso/equipe retorna portal-admin.html"""
        response = client.get("/acesso/equipe")
        assert response.status_code == 200
        # Verificar conteúdo específico
        assert b"Portal" in response.data or b"portal" in response.data.lower()
    
    def test_client_access_route_without_html_extension(self, client):
        """Testa se /acesso/cliente existe (sem .html)"""
        response = client.get("/acesso/cliente")
        assert response.status_code == 200
        assert response.content_type.startswith("text/html")
    
    def test_no_html_extension_in_urls(self, client):
        """Verifica que URLs com .html não funcionam"""
        response = client.get("/acesso/equipe.html")
        assert response.status_code == 404
    
    def test_no_generic_file_route(self, client):
        """Verifica que não há rota genérica de arquivo"""
        response = client.get("/any-random-file.html")
        assert response.status_code == 404


class TestStaticFilesServing:
    """Testes para servimento de arquivos estáticos"""
    
    def test_static_css_portal_exists(self, client):
        """Testa se /static/css/portal.css é servido"""
        response = client.get("/static/css/portal.css")
        assert response.status_code == 200
        assert response.content_type.startswith("text/css")
    
    def test_static_css_team_exists(self, client):
        """Testa se /static/css/team.css é servido"""
        response = client.get("/static/css/team.css")
        assert response.status_code == 200
        assert response.content_type.startswith("text/css")
    
    def test_static_js_portal_exists(self, client):
        """Testa se /static/js/portal.js é servido"""
        response = client.get("/static/js/portal.js")
        assert response.status_code == 200
        assert "application/javascript" in response.content_type or "text/javascript" in response.content_type
    
    def test_static_js_portal_admin_exists(self, client):
        """Testa se /static/js/portal-admin.js é servido"""
        response = client.get("/static/js/portal-admin.js")
        assert response.status_code == 200
        assert "application/javascript" in response.content_type or "text/javascript" in response.content_type
    
    def test_static_js_dashboard_exists(self, client):
        """Testa se /static/js/team/dashboard.js é servido"""
        response = client.get("/static/js/team/dashboard.js")
        assert response.status_code == 200
        assert "application/javascript" in response.content_type or "text/javascript" in response.content_type
    
    def test_nonexistent_static_file_returns_404(self, client):
        """Testa se arquivo estático não existente retorna 404"""
        response = client.get("/static/css/nonexistent.css")
        assert response.status_code == 404


class TestURLCleaness:
    """Testes para verificar que as URLs são limpas (sem .html)"""
    
    @pytest.mark.parametrize("url,expected_status", [
        ("/", 200),
        ("/acesso/equipe", 200),
        ("/acesso/cliente", 200),
    ])
    def test_clean_urls_without_extension(self, client, url, expected_status):
        """Testa se URLs limpas (sem extensão) funcionam"""
        response = client.get(url)
        assert response.status_code == expected_status
    
    @pytest.mark.parametrize("url", [
        "/index.html",
        "/portal-admin.html",
        "/portal-cliente.html",
    ])
    def test_html_extensions_not_accessible(self, client, url):
        """Testa se URLs com .html retornam 404"""
        response = client.get(url)
        assert response.status_code == 404


class TestContentType:
    """Testes para verificar tipos de conteúdo corretos"""
    
    def test_html_files_have_correct_content_type(self, client):
        """Testa se arquivos HTML têm content-type correto"""
        response = client.get("/acesso/equipe")
        assert "text/html" in response.content_type
    
    def test_css_files_have_correct_content_type(self, client):
        """Testa se arquivos CSS têm content-type correto"""
        response = client.get("/static/css/portal.css")
        assert "text/css" in response.content_type
    
    def test_js_files_have_correct_content_type(self, client):
        """Testa se arquivos JS têm content-type correto"""
        response = client.get("/static/js/portal.js")
        assert ("application/javascript" in response.content_type or 
                "text/javascript" in response.content_type)
