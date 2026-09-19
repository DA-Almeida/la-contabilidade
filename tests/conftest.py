"""
Configuração do pytest para testes da aplicação L&A Contabilidade
"""
import sys
from pathlib import Path

# Adicionar o caminho do backend ao sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

import pytest
from app import create_app
from app.extensions import db


@pytest.fixture(scope="session")
def app():
    """Cria a aplicação Flask para testes"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cria um cliente de teste Flask"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Cria um runner de CLI para testes"""
    return app.test_cli_runner()


@pytest.fixture
def app_context(app):
    """Fornece contexto da aplicação para os testes"""
    with app.app_context():
        yield app
