# Plano de Projeto — Site Institucional + Portais Operacionais

## 1. Objetivo

Transformar o layout atual em um sistema real para a L&A Contabilidade, com site público, portal do cliente e área interna do escritório, tudo integrado a backend e banco de dados.

O projeto deve contemplar:

- Site institucional responsivo com seções de apresentação, serviços, sobre, blog, depoimentos, FAQ e contato.
- Integração com WhatsApp e canais de atendimento.
- Portal do cliente com login, documentos, guias, tickets e visão de pendências.
- Área do colaborador/admin com dashboards, clientes, tarefas, agenda, CRM, financeiro, relatórios e controle de permissões.
- Controle de acesso por perfil com menus e rotas protegidos.
- Backend em Python para sustentar autenticação, dados, regras de negócio e integrações.
- Banco de dados relacional para armazenar clientes, colaboradores, tickets, agenda, finanças, documentos e permissões.
- Estrutura pronta para evolução incremental sem depender de regras simuladas no front-end.

---

## 2. Escopo funcional atual

O código existente já indica os módulos que precisam virar implementação real:

- Site público com hero, serviços, sobre, depoimentos, blog, FAQ e contato.
- Menu com acesso para área restrita e links para os portais.
- Formulário de contato com envio real de mensagem.
- Portal do cliente com visualização de documentos, guias, tickets e status.
- Área do colaborador com painel geral, lista de tarefas e visão de produtividade.
- Cadastro e manutenção de colaboradores.
- Cadastro e manutenção de clientes.
- Kanban/tarefas por setor e por responsável.
- Tickets de atendimento com histórico de mensagens.
- Financeiro com receitas, despesas, categorias e formas de pagamento.
- Agenda com compromissos, visitas, reuniões e prazos.
- CRM e funil de leads.
- Controle de validade de documentos e certidões.
- Contas a pagar e a receber.
- Atribuição de responsáveis por setor para cada cliente.

Esse escopo deve ser tratado como produto real, não como mockup visual. As interações mostradas no front-end precisam ser suportadas por API, persistência e autenticação.

---

## 3. Stack inicial

| Componente | Tecnologia |
|---|---|
| Frontend público | HTML + CSS + JavaScript |
| Portais internos | HTML + CSS + JavaScript ou framework equivalente na evolução |
| Backend | Python + Flask em arquitetura MVC |
| Autenticação | JWT + sessão segura |
| Banco de dados | PostgreSQL |
| ORM | SQLAlchemy |
| Migrações | Bootstrap automático de schema com SQLAlchemy |
| Versionamento | Git + GitHub |
| IDE | VS Code |
| Containers | Podman + podman-compose |
| Deploy inicial | Ambiente local |

Observação: o front-end atual pode seguir como base visual, mas as ações devem sair do estado estático e passar a consumir API e banco de dados.

---

## 4. Arquitetura proposta

```text
                    ┌──────────────────────────┐
                    │     Site Público         │
                    │  Institucional e SEO     │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ Portal do Cliente/Admin  │
                    │  Dashboard e operação    │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │   Flask MVC + ORM        │
                    │ Controllers, Services,   │
                    │ Models e integrações     │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │     PostgreSQL           │
                    │ dados + histórico + logs  │
                    └──────────────────────────┘
```

Princípios de arquitetura:

- Adotar padrão MVC no backend, separando controllers, services e models.
- Separar o site institucional dos portais internos.
- Centralizar regras de negócio no backend.
- Padronizar acesso ao banco exclusivamente via ORM com SQLAlchemy.
- Persistir dados críticos no banco, sem depender de arrays estáticos no front-end.
- Proteger áreas internas com autenticação e autorização por perfil.
- Manter módulos independentes por domínio: clientes, colaboradores, tarefas, tickets, agenda, financeiro, CRM, documentos e permissões.
- Garantir bootstrap automático do schema ao subir a aplicação caso tabelas ainda não existam.

---

## 5. Estrutura sugerida do repositório

```text
LA-CONTABILIDADE/
├── site-publico/
│   ├── index.html
│   ├── style.css
│   └── site.js
├── portal-cliente/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── portal-admin/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── backend/
│   ├── run.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   └── routes/
│   └── migrations/
├── database/
│   ├── migrations/
│   └── seeds/
├── tests/
├── podman-compose.yml
├── README.md
└── .gitignore
```

Regra de organização: cada domínio funcional deve ter seu próprio módulo no backend para evitar acoplamento e facilitar manutenção. No backend, rotas encaminham para controllers, controllers delegam regras para services e a persistência fica nos models SQLAlchemy.

---

## 6. Fase 1 — Fundamento técnico

### Objetivo

Preparar a base técnica para que o sistema possa sair do protótipo e virar aplicação funcional.

### Entregas

- Configuração do ambiente local.
- Setup do backend Flask em MVC.
- Setup do PostgreSQL em container com podman-compose.
- Estrutura inicial de autenticação.
- Estrutura inicial de banco, ORM e migrations.
- Padronização de rotas, controllers, serviços e models.

### Tarefas

- [ ] Confirmar ambiente de desenvolvimento.
- [ ] Configurar repositório Git e fluxo de branches.
- [ ] Criar projeto Flask no padrão MVC.
- [ ] Configurar conexão com PostgreSQL via SQLAlchemy.
- [ ] Criar podman-compose do banco de dados.
- [ ] Configurar bootstrap automático do schema caso tabelas não existam.
- [ ] Definir modelo inicial de usuários e perfis.
- [ ] Definir esquema inicial de clientes e colaboradores.
- [ ] Preparar JWT e controle de sessão.
- [ ] Criar base de testes.

---

## 7. Fase 2 — Site público

### Objetivo

Implantar o site institucional com conteúdo real e navegação funcional.

### Módulos

- Hero com CTA para WhatsApp e serviços.
- Seção de serviços com cards e benefícios.
- Sobre a empresa com diferenciais.
- Depoimentos.
- Blog com lista de artigos e categorias.
- FAQ expansível.
- Contato com formulário funcional.
- Rodapé com links, contato e áreas restritas.
- Botão flutuante de WhatsApp.

### Tarefas

- [ ] Tornar os links de navegação funcionais.
- [ ] Integrar formulário de contato ao backend.
- [ ] Persistir leads vindos do site.
- [ ] Preparar conteúdo do blog para backend ou CMS simples.
- [ ] Revisar responsividade e acessibilidade.
- [ ] Validar SEO básico e performance.

---

## 8. Fase 3 — Autenticação e permissões

### Objetivo

Garantir acesso seguro aos portais e separar o que cada perfil pode ver.

### Perfis iniciais

- Admin.
- Colaborador.
- Cliente.

### Regras

- Login com JWT e sessão válida.
- Menus dinâmicos conforme perfil.
- Rota protegida por permissão.
- Acesso ao portal do cliente restrito ao seu próprio conteúdo.
- Acesso do colaborador restrito ao seu setor quando aplicável.

### Tarefas

- [ ] Criar cadastro de usuários autenticáveis.
- [ ] Criar login e logout reais.
- [ ] Definir middleware de autenticação.
- [ ] Implementar autorização por perfil.
- [ ] Registrar tentativas e auditoria básica.

---

## 9. Fase 4 — Portal do cliente

### Objetivo

Entregar a experiência mostrada no layout com documentos, guias e tickets reais.

### Módulos

- Visão geral do cliente.
- Pendências de documentos.
- Documentos enviados e recebidos.
- Checklist mensal.
- Tickets de suporte.
- Mensagens e histórico de atendimento.

### Tarefas

- [ ] Modelar documentos do cliente.
- [ ] Modelar tickets e mensagens.
- [ ] Criar painel de status do cliente.
- [ ] Permitir envio de arquivos e anexos.
- [ ] Exibir pendências e histórico por período.

---

## 10. Fase 5 — Área do colaborador e administração

### Objetivo

Substituir os dados simulados por gestão operacional real do escritório.

### Módulos

- Dashboard geral.
- Gestão de colaboradores.
- Gestão de clientes.
- Kanban de tarefas.
- Agenda interna.
- CRM e funil de leads.
- Financeiro.
- Relatórios.
- Controle de validade de documentos.
- Contas a pagar e a receber.

### Tarefas

- [ ] Criar CRUD de colaboradores.
- [ ] Criar CRUD de clientes.
- [ ] Persistir tarefas com status e responsável.
- [ ] Persistir agenda e compromissos.
- [ ] Persistir leads e estágio comercial.
- [ ] Persistir receitas, despesas e contas.
- [ ] Criar filtros por setor e por status.
- [ ] Implementar atribuição de responsáveis por cliente.

---

## 11. Fase 6 — Workflow operacional

### Objetivo

Organizar os processos internos em um fluxo simples e rastreável, sem depender de engine BPM pesada.

### Modelo proposto

```text
Criado
  ↓
Em análise
  ↓
Em andamento
  ↓
Aguardando cliente
  ↓
Concluído
```

### Regras

- Cada tarefa deve ter status, prazo, setor e responsável.
- Tickets devem ter histórico de mensagens.
- Alterações devem gerar log de evento.
- Cada mudança de status deve ser validada pelo backend.

### Tarefas

- [ ] Definir estados oficiais do workflow.
- [ ] Criar histórico de transições.
- [ ] Definir regras por perfil e setor.
- [ ] Implementar filtros e dashboards por situação.

---

## 12. Fase 7 — Validações, relatórios e integração

### Objetivo

Garantir consistência dos dados e visão gerencial.

### Entregas

- Relatórios de tarefas, clientes e financeiro.
- Alertas de vencimento e documentos próximos do prazo.
- Indicadores de produtividade por colaborador.
- Visões consolidadas para administração.

### Tarefas

- [ ] Criar consultas consolidadas.
- [ ] Criar relatórios de produtividade.
- [ ] Criar alertas de vencimento.
- [ ] Criar exportações básicas quando necessário.

---

## 13. Fase 8 — Testes e preparação para publicação

### Objetivo

Validar a aplicação antes de colocar em produção.

### Tarefas

- [ ] Testar autenticação e permissões.
- [ ] Testar CRUDs principais.
- [ ] Testar fluxo do portal do cliente.
- [ ] Testar workflow de tarefas e tickets.
- [ ] Testar envio de formulário público.
- [ ] Testar responsividade em mobile.
- [ ] Preparar deploy em ambiente estável.

---

## 14. Prioridade recomendada

Se for executar por etapas, a ordem ideal é:

1. Base técnica e banco.
2. Autenticação e permissões.
3. Portal do cliente.
4. Área interna com clientes, tarefas e tickets.
5. Financeiro, CRM, agenda e relatórios.
6. Ajustes de UX, SEO e publicação.

---

## 15. Próximo passo imediato

O próximo passo não é criar novas telas estáticas, e sim transformar os dados simulados do front-end em API, banco e autenticação reais. Isso evita retrabalho e alinha o projeto ao que já foi desenhado no site.

Exemplos de endpoints:

```text
GET    /api/solicitacoes
POST   /api/solicitacoes
GET    /api/tarefas
GET    /api/tarefas/<id>
POST   /api/tarefas/<id>/aprovar
POST   /api/tarefas/<id>/rejeitar
POST   /api/tarefas/<id>/atualizar-status
```

### Tarefas

- [ ] Criar aplicação Flask.
- [ ] Criar estrutura de rotas.
- [ ] Configurar variáveis de ambiente.
- [ ] Configurar conexão PostgreSQL.
- [ ] Criar camada de serviços.
- [ ] Implementar o motor de workflow em Python.
- [ ] Criar módulo de autenticação com JWT.
- [ ] Criar módulo de autorização por perfil.
- [ ] Validar sessão ativa em todas as rotas protegidas.
- [ ] Criar módulo de branding/whitelabel.
- [ ] Persistir título do site e logo no banco.
- [ ] Expor endpoints de configuração visual para administração.
- [ ] Criar módulo de cadastro de funcionários.
- [ ] Criar relacionamento entre usuário e perfil.
- [ ] Criar menu dinâmico por perfil.
- [ ] Criar tratamento de erros.
- [ ] Criar logs.
- [ ] Criar testes básicos da API.

---

# 9. Fase 4 — Criar o frontend

O frontend será totalmente personalizado.

A ideia é não ficar preso a uma interface genérica e sim criar um painel próprio para o negócio.

Tecnologias:

```text
HTML
CSS
JavaScript
Bootstrap
```

Exemplo de interface:

```text
┌──────────────────────────────────────────────┐
│              SISTEMA DE PROCESSOS            │
├─────────────┬────────────────────────────────┤
│             │                                │
│ Dashboard   │  Minhas tarefas                │
│             │                                │
│ Processos   │  ┌──────────────────────────┐  │
│             │  │ Aprovar solicitação       │  │
│ Tarefas     │  │ Cliente: Empresa XYZ     │  │
│             │  │ Status: Pendente          │  │
│ Relatórios  │  │ [Abrir]                  │  │
│             │  └──────────────────────────┘  │
│             │                                │
└─────────────┴────────────────────────────────┘
```

### Tarefas

- [ ] Criar layout principal.
- [ ] Criar menu lateral dinâmico por perfil.
- [ ] Criar dashboard.
- [ ] Criar tela de tarefas.
- [ ] Criar tela de detalhes da tarefa.
- [ ] Criar formulários.
- [ ] Criar área de administração do whitelabel.
- [ ] Permitir alterar título do site na interface administrativa.
- [ ] Permitir alterar logo do site na interface administrativa.
- [ ] Criar tela de login com JWT.
- [ ] Criar tela de cadastro de funcionários.
- [ ] Criar mensagens de sucesso/erro.
- [ ] Tornar interface responsiva.
- [ ] Testar no celular.
- [ ] Integrar frontend com Flask.

---

# 10. Fase 5 — Integrar Frontend + Flask + Workflow Interno

Fluxo esperado:

```text
Usuário
   │
   ▼
Site BPM / Frontend
   │
   ▼
Flask API
   │
   ├──────────────► PostgreSQL
   │
   └──────────────► Workflow interno
                         │
                         ▼
                    Status e regras
```

Exemplo:

1. Usuário abre uma solicitação.
2. Frontend envia POST para Flask.
3. Flask grava os dados no PostgreSQL.
4. Flask valida regras de transição.
5. O status muda conforme a etapa.
6. Frontend consulta as tarefas.
7. Usuário executa a ação de aprovação ou rejeição.
8. Flask atualiza o histórico e o status.
9. A solicitação avança ou encerra o processo.

---

# 11. Fase 6 — Persistência dos dados

Separar os dados de negócio dos dados de execução do workflow.

Exemplo:

```text
PostgreSQL

┌─────────────────────┐
│ solicitacoes        │
├─────────────────────┤
│ id                  │
│ descricao           │
│ solicitante         │
│ status              │
│ criado_em           │
└─────────────────────┘

┌─────────────────────┐
│ historico           │
├─────────────────────┤
│ id                  │
│ solicitacao_id      │
│ usuario             │
│ acao                │
│ data                │
└─────────────────────┘
```

O próprio backend fica responsável pela **regra de transição do workflow**, enquanto o PostgreSQL mantém os **dados de negócio** que a aplicação precisa.

---

# 12. Fase 7 — GitHub

Tudo deve ser versionado.

### Primeiro commit

```bash
git init
git add .
git commit -m "Initial project structure"
```

### Fluxo recomendado

```text
main
 │
 ├── develop
 │
 ├── feature/frontend
 │
 ├── feature/workflow-python
 │
 └── feature/backend
```

Para cada alteração:

```bash
git checkout -b feature/nova-funcionalidade

git add .
git commit -m "Add nova funcionalidade"

git push origin feature/nova-funcionalidade
```

Depois, abrir Pull Request para `develop` ou `main`.

---

# 13. Fase 8 — Containers

Criar uma stack reproduzível.

Exemplo conceitual:

```text
┌─────────────────────────────────┐
│          docker-compose         │
│                                 │
│  ┌─────────┐   ┌────────────┐  │
│  │  API    │   │ PostgreSQL │  │
│  │ Python  │   │            │  │
│  └─────────┘   └────────────┘  │
│                                 │
│  ┌─────────┐                    │
│  │ Flask   │                    │
│  └─────────┘                    │
│                                 │
└─────────────────────────────────┘
```

### Tarefas

- [ ] Criar Dockerfile do backend.
- [ ] Criar compose.
- [ ] Configurar PostgreSQL.
- [ ] Configurar API Python/Flask.
- [ ] Configurar volumes.
- [ ] Configurar variáveis de ambiente.
- [ ] Testar `up`.
- [ ] Testar `down`.
- [ ] Documentar instalação.

---

# 14. Fase 9 — Qualidade

Depois que o MVP funcionar:

- [ ] Adicionar autenticação.
- [ ] Adicionar autorização.
- [ ] Criar usuários e perfis.
- [ ] Criar suporte a múltiplos clientes whitelabel.
- [ ] Validar JWT em todas as rotas.
- [ ] Validar permissão por rota e perfil.
- [ ] Criar logs.
- [ ] Criar auditoria.
- [ ] Criar testes automatizados.
- [ ] Validar tratamento de erros.
- [ ] Melhorar UX.
- [ ] Melhorar responsividade.
- [ ] Adicionar documentação da API.

---

# 15. Fase 10 — Deploy

Somente depois de o projeto funcionar localmente.

Possibilidades:

```text
Servidor Linux
     │
     ├── Podman/Docker
     │
     ├── Flask ou API Python
     ├── PostgreSQL
     └── Motor de workflow
```

Posteriormente, a mesma aplicação pode evoluir para:

```text
                    Internet
                       │
                    Cloudflare
                       │
                  Reverse Proxy
                       │
             ┌─────────┴─────────┐
             │                   │
          Frontend             API
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                 Python                  PostgreSQL
```

---

# 16. MVP — Primeira versão

Não tentar construir tudo de uma vez.

A primeira versão deve ter somente:

```text
1. Usuário abre solicitação
        ↓
2. API Python inicia o fluxo
        ↓
3. Analista recebe tarefa
        ↓
4. Analista aprova ou rejeita
        ↓
5. Sistema atualiza o status
        ↓
6. Interface mostra o resultado
```

### MVP Checklist

- [ ] PostgreSQL funcionando.
- [ ] Flask funcionando.
- [ ] Frontend funcionando.
- [ ] Frontend conversando com Flask.
- [ ] Flask validando status do workflow.
- [ ] Flask conversando com PostgreSQL.
- [ ] Processo completo funcionando.
- [ ] Histórico de ações funcionando.
- [ ] JWT funcionando em todas as rotas protegidas.
- [ ] Permissões por perfil funcionando.
- [ ] Menu dinâmico por perfil funcionando.
- [ ] Admin de whitelabel funcionando.
- [ ] Título do site alterável pela administração.
- [ ] Logo do site alterável pela administração.
- [ ] Cadastro de funcionários funcionando.
- [ ] Código no GitHub.
- [ ] Projeto executável através de containers.
- [ ] README explicando como executar.

---

# 17. Evolução futura

Depois do MVP:

```text
MVP
 │
 ├── Autenticação
 ├── RBAC
 ├── Notificações
 ├── Upload de arquivos
 ├── Dashboard
 ├── Relatórios
 ├── Auditoria
 ├── SLA
 ├── Métricas
 ├── Integrações REST
 ├── Integração com sistemas externos
 └── Deploy em cloud
```

---

# 18. Regra principal do projeto

**Não colocar regra de negócio complexa dentro do HTML.**

Responsabilidades:

```text
HTML/CSS/JS
    → Interface

Flask
    → API + regras de negócio + transição do workflow

PostgreSQL
    → Dados de negócio + histórico + status

GitHub
    → Versionamento
```

Essa separação facilita manutenção, testes e evolução, sem depender de uma infraestrutura pesada de BPM.

---

# 19. Objetivo final

Ao terminar o projeto, você terá uma aplicação de gestão interna com:

- Workflow customizado por etapas.
- Interface web própria.
- Backend REST.
- Banco PostgreSQL.
- Histórico de ações e status.
- Containers.
- Git/GitHub.
- Testes.
- Documentação.
- Possibilidade de deploy.

E o mais importante: **todo o desenvolvimento inicial pode ser feito localmente e sem depender de serviços pagos ou motores de workflow pesados.**
