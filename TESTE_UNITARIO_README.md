

## 🧩 Estrutura de um Teste

### Exemplo: Teste de Rota Pública

```python
def test_home_route_returns_200(self, client):
    """Testa se a rota / retorna status 200"""
    response = client.get("/")
    assert response.status_code == 200
```

### Exemplo: Teste Parametrizado

```python
@pytest.mark.parametrize("url,expected_status", [
    ("/", 200),
    ("/acesso/equipe", 200),
])
def test_clean_urls(self, client, url, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status
```

## 🔧 Fixtures Disponíveis

- **`app`**: Aplicação Flask configurada para testes
- **`client`**: Cliente para fazer requisições
- **`runner`**: CLI runner para testes de comandos
- **`app_context`**: Contexto da aplicação

## ✅ Checklist Antes de Commit

- [ ] Rodou `pytest -v` e todos passaram
- [ ] Rodou `pytest --cov` 
- [ ] Todas as rotas têm testes

---

**Status**: ✅ Testes prontos para rodar

