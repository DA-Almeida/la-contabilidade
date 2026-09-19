# L&A Contabilidade

## Roles existentes

As roles válidas no sistema são definidas em `backend/app/services/auth_service.py` e atualmente são:

- `admin`: acesso total ao painel interno e gestão de usuários
- `colaborador`: acesso ao painel interno operacional
- `cliente`: acesso ao portal do cliente

A validação usada pelo backend é:

```python
VALID_ROLES = {"admin", "colaborador", "cliente"}
```

## Primeira execução

1. Copie `.env.example` para `.env` e altere `SECRET_KEY`.
2. Suba o banco com `podman-compose up -d`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Inicie o sistema: `python backend/run.py`.
5. Abra `http://127.0.0.1:5000` no navegador. O site público e a API são atendidos pela mesma aplicação.

Na primeira instalação, quando ainda não existe nenhum usuário no banco, pode-se criar o primeiro administrador com a rota de bootstrap:

```bash
curl -X POST http://localhost:5000/api/auth/bootstrap \
  -H 'Content-Type: application/json' \
  -d '{"name":"Administrador","email":"admin@exemplo.com","password":"uma-senha-segura"}'
```

Depois do primeiro acesso, a criação de usuários deve ser feita pela área administrativa autenticada, com a rota protegida `POST /api/users`.

Exemplo de payload para criar um usuário `admin`:

```json
{
  "name": "Administrador",
  "email": "admin@exemplo.com",
  "password": "minhaSenha123",
  "role": "admin"
}
```

Comando de exemplo:

```bash
curl -X POST http://localhost:5000/api/users \
  -H 'Content-Type: application/json' \
  -d '{"name":"Administrador","email":"admin@exemplo.com","password":"minhaSenha123","role":"admin"}'
```

Depois disso, `POST /api/auth/login` cria uma sessão JWT em cookie `HttpOnly`. `GET /api/leads` requer sessão válida e o perfil `admin` ou `colaborador`.

Os acessos públicos são `http://127.0.0.1:5000/acesso/equipe` e `http://127.0.0.1:5000/acesso/cliente`. Após o login, as rotas protegidas são `/portal/equipe` e `/portal/cliente`; elas validam a sessão e o perfil no servidor antes de entregar o portal.
