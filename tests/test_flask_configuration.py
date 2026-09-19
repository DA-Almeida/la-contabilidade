"""
Testes para configuração da aplicação Flask
"""
import pytest
from pathlib import Path


class TestFlaskConfiguration:
    """Testes para configuração do Flask"""
    
    def test_app_is_created(self, app):
        """Testa se a aplicação Flask é criada corretamente"""
        assert app is not None
    
    def test_app_is_flask_instance(self, app):
        """Testa se a aplicação é uma instância do Flask"""
        from flask import Flask
        assert isinstance(app, Flask)
    
    def test_app_testing_mode_enabled(self, app):
        """Testa se o modo de testes está ativado"""
        assert app.config["TESTING"] is True


class TestStaticFolderConfiguration:
    """Testes para configuração da pasta estática"""
    
    def test_static_folder_is_configured(self, app):
        """Testa se a pasta estática está configurada"""
        assert app.static_folder is not None
    
    def test_static_folder_exists(self, app):
        """Testa se a pasta estática existe no sistema de arquivos"""
        static_path = Path(app.static_folder)
        assert static_path.exists(), f"Pasta estática não existe em {static_path}"
    
    def test_static_url_path_is_correct(self, app):
        """Testa se o URL path para estáticos está correto"""
        assert app.static_url_path == "/static"
    
    def test_static_folder_contains_css(self, app):
        """Testa se a pasta estática contém CSS"""
        static_path = Path(app.static_folder)
        css_path = static_path / "css"
        assert css_path.exists(), f"Pasta css não existe em {static_path}"
    
    def test_static_folder_contains_js(self, app):
        """Testa se a pasta estática contém JS"""
        static_path = Path(app.static_folder)
        js_path = static_path / "js"
        assert js_path.exists(), f"Pasta js não existe em {static_path}"
    
    def test_portal_css_file_exists(self, app):
        """Testa se portal.css existe"""
        static_path = Path(app.static_folder)
        portal_css = static_path / "css" / "portal.css"
        assert portal_css.exists(), f"Arquivo portal.css não existe em {portal_css}"
    
    def test_portal_js_file_exists(self, app):
        """Testa se portal.js existe"""
        static_path = Path(app.static_folder)
        portal_js = static_path / "js" / "portal.js"
        assert portal_js.exists(), f"Arquivo portal.js não existe em {portal_js}"


class TestBlueprintRegistration:
    """Testes para registro de blueprints"""
    
    def test_public_blueprint_registered(self, app):
        """Testa se o blueprint público está registrado"""
        assert "public" in app.blueprints
    
    def test_auth_blueprint_registered(self, app):
        """Testa se o blueprint de autenticação está registrado"""
        assert "auth" in app.blueprints
    
    def test_blueprints_have_routes(self, app):
        """Testa se os blueprints têm rotas registradas"""
        with app.app_context():
            routes = [str(rule) for rule in app.url_map.iter_rules()]
            # Verificar algumas rotas principais
            assert any("/" in route for route in routes)
            assert any("acesso" in route for route in routes)
            assert any("api/auth" in route for route in routes)


class TestApplicationContext:
    """Testes para contexto da aplicação"""
    
    def test_app_context_can_be_created(self, app):
        """Testa se o contexto da aplicação pode ser criado"""
        with app.app_context():
            # Deve estar dentro do contexto
            from flask import current_app
            assert current_app is not None
    
    def test_database_initialized(self, app_context):
        """Testa se o banco de dados está inicializado"""
        from app.extensions import db
        assert db is not None
        assert db.engine is not None
