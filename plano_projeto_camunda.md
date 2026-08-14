# Plano de Projeto — Frontend + Flask + PostgreSQL + Workflow Interno

## 1. Objetivo

Construir um sistema de gestão operacional com workflow leve, baseado em tarefas/etapas, implementado em Python no próprio backend, com infraestrutura simples de manter.

- Interface web personalizada e responsiva.
- Backend em Python + Flask.
- PostgreSQL como banco de dados.
- Workflow interno simples, tipo ticket/kanban.
- Projeto whitelabel com branding configurável por cliente.
- Página administrativa para alterar título do site e logo.
- Controle de acesso por perfil e permissões.
- Sessão protegida por JWT e validação de rota por usuário logado.
- Menu dinâmico conforme permissões do perfil.
- Cadastro de funcionários com perfis e acesso distintos.
- Execução local utilizando containers.
- Stack inicialmente 100% gratuita.
- Estrutura preparada para futuramente publicar em um servidor.

---

## 2. Stack inicial

| Componente | Tecnologia |
|---|---|
| Workflow | Fluxo interno por etapas e tickets |
| Modelagem | Estados e regras próprias da aplicação |
| Frontend | HTML + CSS + JavaScript |
| UI | Bootstrap |
| Backend | Python + Flask |
| Banco de dados | PostgreSQL |
| Versionamento | Git + GitHub |
| IDE | VS Code |
| Containers | Podman ou Docker |
| SO de desenvolvimento | Fedora |
| Hospedagem inicial | Máquina local |

> Para este momento, a recomendação é desenvolver o workflow diretamente em Python, com regras simples e gerenciamento de status em base de dados. Isso reduz infraestrutura, acelera o desenvolvimento e se encaixa melhor no atual nível de operação.

---

## 3. Arquitetura proposta

```text
                    ┌──────────────────────┐
                    │      Site Público    │
                    │   Landing page / SEO │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Site BPM        │
                    │  Gestão interna / UI │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Python / Flask    │
                    │   API da aplicação   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │ tickets + histórico  │
                    └──────────────────────┘
```

O princípio será separar claramente:

- **Site público:** responsável pela apresentação externa, landing page e comunicação institucional.
- **Site BPM:** responsável pela interface interna do sistema operacional.
- **Flask:** responsável pelas regras e APIs da aplicação.
- **PostgreSQL:** responsável pelos dados da aplicação e pelo histórico de tarefas.
- **Workflow interno:** gerenciado por status e regras próprias do sistema, em vez de um motor de BPM pesado.
- **Whitelabel / Administração:** responsável por permitir alterar o título do site, o logo e outros elementos visuais por cliente.
- **Autenticação e autorização:** responsável por validar JWT, sessão ativa, perfil e permissões de acesso.
- **Cadastro de funcionários:** responsável por manter usuários, perfis, status e vínculos de acesso.
- **GitHub:** responsável pelo versionamento.

Esses dois sites serão independentes em estrutura e objetivos: um voltado para divulgação e outro para uso interno do negócio e gestão do processo. Além disso, haverá uma área administrativa do sistema para personalizar a marca do cliente e um sistema de segurança com perfis, JWT e controle de acesso por rota e menu.

---

# 4. Estrutura do repositório

Sugestão inicial para o projeto com nome oficial `LA-CONTABILIDADE`:

```text
LA-CONTABILIDADE/
│
├── site-publico/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── assets/
│
├── site-bpm/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── assets/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── admin/
│   │   └── branding.py
│   └── workflow/
│       ├── status.py
│       └── regras.py
│
├── database/
│   └── migrations/
│
├── tests/
│
├── docker-compose.yml
│
├── .gitignore
├── README.md
└── LICENSE
```

Observação: o `site-publico` será a área de apresentação e marketing do projeto, separada do `site-bpm`, que será a interface interna de operação do workflow e da contabilidade. Essa separação evita misturar experiência pública com experiência operacional.

Regra de arquitetura: cada workflow de cada subtarefa deve ser desenvolvido em um arquivo separado, seguindo o princípio de responsabilidade única (`single responsibility`). Isso torna cada fluxo mais simples de testar, evoluir e corrigir sem acoplar regras de diferentes processos.

Regra de segurança: todas as rotas da aplicação devem validar se a sessão está ativa por JWT e, em seguida, verificar se o usuário logado possui autorização para acessar a rota solicitada. O menu deve ser renderizado dinamicamente com base no perfil do usuário autenticado.

---

# 5. Fase 1 — Preparar o ambiente

## Objetivo

Ter tudo funcionando localmente antes de começar o desenvolvimento.

### Tarefas

- [ ] Confirmar versão do Fedora.
- [ ] Instalar/configurar Git.
- [ ] Configurar GitHub.
- [ ] Instalar VS Code.
- [ ] Configurar Python.
- [ ] Criar ambiente virtual Python.
- [ ] Instalar Flask.
- [ ] Instalar PyJWT.
- [ ] Instalar Podman ou Docker.
- [ ] Testar containers.
- [ ] Subir PostgreSQL em container.
- [ ] Definir workflow interno de etapas.
- [ ] Definir regras de transição de status.
- [ ] Definir perfis: admin, gerente, supervisor e analista.

---

# 6. Recomendação de workflow para esta fase

A melhor opção neste momento é um workflow simples baseado em tickets e etapas, com status explícitos e regras próprias da aplicação.

Exemplo:

```text
Aberta
  ↓
Em análise
  ↓
Pendente
  ↓
Aprovada / Rejeitada
  ↓
Concluída
```

### Vantagens

- Sem infraestrutura pesada.
- Sem container de engine BPM.
- Fácil de manter e evoluir.
- Mais adequado ao que você já planeja desenvolver.
- Permite versionamento e controle sem depender de engine externa.

### Estrutura sugerida do workflow

- `aberta`: nova solicitação criada.
- `em_analise`: tarefa em revisão.
- `pendente`: depende de informação ou ação.
- `aprovada`: processo aceita.
- `rejeitada`: processo recusado.
- `concluida`: finalizada.

Cada transição pode ser controlada no backend com validações simples, sem precisar de um motor de workflow externo.

Além disso, cada perfil terá permissões específicas:

- **admin**: acesso total ao sistema, configuração, usuários e branding.
- **gerente**: acesso operacional e gestão de equipe.
- **supervisor**: acompanhamento e aprovação de rotas específicas.
- **analista**: execução de tarefas operacionais e consulta limitada.

Regra prática: cada tipo de processo ou subtarefa deve ter seu próprio arquivo de workflow, por exemplo:

```text
backend/workflow/
├── solicitacao.py
├── aprovacao.py
├── rejeicao.py
├── fechamento.py
└── historico.py
```

Cada arquivo será responsável por uma parte do fluxo, mantendo uma responsabilidade única.

---

# 7. Fase 2 — Criar o fluxo interno de processo

Começar com um processo extremamente simples e customizado.

Exemplo:

```text
Início
  ↓
Solicitação
  ↓
Análise
  ↓
Decisão
  ↓
Finalização
  ↓
Fim
```

### Tarefas

- [ ] Criar tabela de solicitações.
- [ ] Definir status do processo.
- [ ] Criar regras de transição.
- [ ] Criar histórico de ações.
- [ ] Criar lógica de aprovação e rejeição.
- [ ] Validar fluxo em ambiente local.
- [ ] Testar operação por usuário.

---

# 8. Fase 3 — Criar o backend Flask

Criar uma API responsável por gerenciar o workflow interno e o PostgreSQL.

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
