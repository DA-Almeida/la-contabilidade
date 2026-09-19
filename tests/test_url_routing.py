"""
Testes para roteamento de URLs e headers
"""
import pytest


class TestURLRouting:
    """Testes para verificar que o roteamento de URLs está correto"""
    
    def test_clean_urls_are_preferred(self, client):
        """Testa se URLs limpas funcionam corretamente"""
        routes = [
            ("/", 200),
            ("/acesso/equipe", 200),
            ("/acesso/cliente", 200),
        ]
        for route, expected_status in routes:
            response = client.get(route)
            assert response.status_code == expected_status, f"Rota {route} retornou {response.status_code}"
    
    def test_html_extensions_are_not_used(self, client):
        """Testa se extensões .html não são usadas nas URLs"""
        blocked_routes = [
            "/index.html",
            "/portal-admin.html",
            "/portal-cliente.html",
        ]
        for route in blocked_routes:
            response = client.get(route)
            assert response.status_code == 404, f"Rota {route} com .html deveria retornar 404"
    
    def test_generic_file_route_does_not_exist(self, client):
        """Testa se não há rota genérica de arquivo"""
        response = client.get("/some-random-file.html")
        assert response.status_code == 404


class TestResponseHeaders:
    """Testes para verificar headers de resposta"""
    
    def test_html_response_has_correct_headers(self, client):
        """Testa se respostas HTML têm headers corretos"""
        response = client.get("/")
        assert response.headers.get("Content-Type").startswith("text/html")
    
    def test_css_response_has_correct_headers(self, client):
        """Testa se respostas CSS têm headers corretos"""
        response = client.get("/static/css/portal.css")
        assert "text/css" in response.headers.get("Content-Type")
    
    def test_js_response_has_correct_headers(self, client):
        """Testa se respostas JS têm headers corretos"""
        response = client.get("/static/js/portal.js")
        content_type = response.headers.get("Content-Type")
        assert ("application/javascript" in content_type or "text/javascript" in content_type)
