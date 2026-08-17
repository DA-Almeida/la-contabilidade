# L&A Contabilidade

## Primeira execução

1. Copie `.env.example` para `.env` e altere `SECRET_KEY`.
2. Suba o banco com `podman-compose up -d`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Inicie o sistema: `python backend/run.py`.
5. Abra `http://127.0.0.1:5000` no navegador. O site público e a API são atendidos pela mesma aplicação.

Na primeira instalação, crie o administrador com uma única chamada:

```bash
curl -X POST http://localhost:5000/api/auth/bootstrap \
  -H 'Content-Type: application/json' \
  -d '{"name":"Administrador","email":"admin@exemplo.com","password":"uma-senha-segura"}'
```

Depois disso, `POST /api/auth/login` cria uma sessão JWT em cookie `HttpOnly`. `GET /api/leads` requer sessão válida e o perfil `admin` ou `colaborador`.

Os acessos públicos são `http://127.0.0.1:5000/acesso/equipe` e `http://127.0.0.1:5000/acesso/cliente`. Após o login, as rotas protegidas são `/portal/equipe` e `/portal/cliente`; elas validam a sessão e o perfil no servidor antes de entregar o portal.
