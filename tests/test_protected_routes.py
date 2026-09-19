"""
Testes para rotas protegidas (com autenticação)
"""
import pytest


class TestProtectedRoutes:
    """Testes para rotas que requerem autenticação"""
    
    def test_portal_equipe_without_auth_redirects(self, client):
        """Testa se /portal/equipe sem autenticação redireciona"""
        response = client.get("/portal/equipe", follow_redirects=False)
        # Pode ser 302 (redirect) ou 401 (unauthorized)
        assert response.status_code in [302, 401]
    
    def test_portal_equipe_clientes_without_auth_redirects(self, client):
        """Testa se /portal/equipe/clientes sem autenticação redireciona"""
        response = client.get("/portal/equipe/clientes", follow_redirects=False)
        assert response.status_code in [302, 401]
    
    def test_portal_equipe_colaboradores_without_auth_redirects(self, client):
        """Testa se /portal/equipe/colaboradores sem autenticação redireciona"""
        response = client.get("/portal/equipe/colaboradores", follow_redirects=False)
        assert response.status_code in [302, 401]
    
    def test_portal_equipe_tarefas_without_auth_redirects(self, client):
        """Testa se /portal/equipe/tarefas sem autenticação redireciona"""
        response = client.get("/portal/equipe/tarefas", follow_redirects=False)
        assert response.status_code in [302, 401]
    
    def test_portal_equipe_usuarios_without_auth_redirects(self, client):
        """Testa se /portal/equipe/usuarios sem autenticação redireciona"""
        response = client.get("/portal/equipe/usuarios", follow_redirects=False)
        assert response.status_code in [302, 401]
    
    def test_portal_cliente_without_auth_redirects(self, client):
        """Testa se /portal/cliente sem autenticação redireciona"""
        response = client.get("/portal/cliente", follow_redirects=False)
        assert response.status_code in [302, 401]


class TestProtectedRoutesExist:
    """Testes para verificar que todas as rotas protegidas existem"""
    
    @pytest.mark.parametrize("route", [
        "/portal/equipe",
        "/portal/equipe/clientes",
        "/portal/equipe/colaboradores",
        "/portal/equipe/tarefas",
        "/portal/equipe/atribuicoes",
        "/portal/equipe/tickets",
        "/portal/equipe/guias",
        "/portal/equipe/obrigacoes",
    ])
    def test_protected_routes_exist(self, client, route):
        """Testa se rotas protegidas existem (sem .html no URL)"""
        # Mesmo sem autenticação, deve ser 302/401, não 404
        response = client.get(route, follow_redirects=False)
        assert response.status_code != 404, f"Rota {route} não existe"
    
    def test_protected_routes_not_with_html_extension(self, client):
        """Testa se URLs com .html retornam 404 em rotas protegidas"""
        response = client.get("/portal/equipe.html", follow_redirects=False)
        assert response.status_code == 404


class TestCleanURLsInProtectedRoutes:
    """Testes para verificar URLs limpas em rotas protegidas"""
    
    @pytest.mark.parametrize("url_with_html,url_without_html", [
        ("/portal/equipe.html", "/portal/equipe"),
        ("/portal/equipe/clientes.html", "/portal/equipe/clientes"),
        ("/portal/cliente.html", "/portal/cliente"),
    ])
    def test_html_extension_not_used(self, client, url_with_html, url_without_html):
        """Testa se .html é rejeitado mas URL sem extensão existe"""
        response_with_html = client.get(url_with_html, follow_redirects=False)
        response_without_html = client.get(url_without_html, follow_redirects=False)
        
        # Com .html deve ser 404
        assert response_with_html.status_code == 404
        # Sem .html não deve ser 404 (pode ser 302/401 por causa da autenticação)
        assert response_without_html.status_code != 404
