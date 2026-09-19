# Guia de Uso - Área da Equipe (Refatorada)

## 🚀 Começando

### 1. Acessar a Área da Equipe

**URL de Login:**
```
http://localhost:5000/acesso/equipe
```

Credenciais para testes:
- Email: admin@example.com (ou um colaborador)
- Senha: (configurada no banco de dados)

### 2. Após Login

Você será redirecionado para:
```
http://localhost:5000/portal/equipe
```

### 3. Navegação

A navbar no topo possui um link "L&A Contabilidade" que funciona como brand.
Use a URL diretamente para acessar cada seção:

- `/portal/equipe` - Dashboard
- `/portal/equipe/clientes` - Gestão de Clientes
- `/portal/equipe/colaboradores` - Gestão de Colaboradores
- `/portal/equipe/tarefas` - Kanban de Tarefas
- `/portal/equipe/atribuicoes` - Atribuições por Setor
- `/portal/equipe/tickets` - Tickets de Suporte
- `/portal/equipe/guias` - Guias e Publicações
- `/portal/equipe/obrigacoes` - Obrigações Fiscais
- `/portal/equipe/usuarios` - Gerenciamento de Usuários (admin only)

## 📱 Dashboard

**URL:** `http://localhost:5000/portal/equipe`

Exibe 7 cards com:
- Leads recebidos
- Clientes ativos
- Colaboradores
- Tarefas abertas
- Tickets abertos
- Guias pendentes
- Obrigações pendentes

## 👥 Clientes

**URL:** `http://localhost:5000/portal/equipe/clientes`

### Cadastrar novo cliente:
1. Preencha o formulário à esquerda
2. Campos obrigatórios: Razão social, CNPJ/CPF, Tipo, Regime
3. Clique em "Salvar cliente"
4. A tabela à direita atualiza automaticamente

### Visualizar clientes:
- Tabela à direita mostra todos os clientes cadastrados
- Campos: Razão Social, CNPJ/CPF, Regime, Mensalidade, Status
- Status mostrado em badge (ativo/inativo)
- Clique no botão de refresh para atualizar manualmente

## 👔 Colaboradores

**URL:** `http://localhost:5000/portal/equipe/colaboradores`

### Cadastrar novo colaborador:
1. Preencha o formulário à esquerda
2. Campos obrigatórios: Nome, E-mail, Departamento, Cargo
3. Opcionalmente selecione um usuário da equipe
4. Clique em "Salvar colaborador"
5. A tabela atualiza automaticamente

### Visualizar colaboradores:
- Tabela à direita mostra todos os colaboradores
- Campos: Nome (com email), Departamento, Cargo, Status
- Status: ativo/inativo/afastado
- A lista de usuários se atualiza conforme você cadastra colaboradores

## 📋 Páginas em Desenvolvimento

As seguintes páginas possuem apenas interface de placeholder:

- **Tarafas** (`/portal/equipe/tarefas`): Kanban com colunas de workflow
- **Atribuições** (`/portal/equipe/atribuicoes`): Atribuição de clientes por setor
- **Tickets** (`/portal/equipe/tickets`): Gestão de suporte ao cliente
- **Guias** (`/portal/equipe/guias`): Publicação de guias e documentos
- **Obrigações** (`/portal/equipe/obrigacoes`): Calendário de obrigações fiscais
- **Usuários** (`/portal/equipe/usuarios`): Admin panel (admin only)

## 🛠️ Funcionalidades Técnicas

### Mensagens de Feedback

Cada formulário mostra:
- ✅ Mensagens verdes para sucesso
- ❌ Mensagens vermelhas para erro

### Validação de Dados

- Campos marcados com * são obrigatórios
- Validação no cliente (HTML) e servidor (Flask)

### Responsividade

- **Desktop**: Layouts side-by-side otimizados
- **Tablet**: Ajustes automáticos
- **Mobile**: Layouts empilhados verticalmente

### Autenticação

- Cada página verifica autenticação ao carregar
- Se você fizer logout, será redirecionado para `/acesso/equipe`
- Sessão armazenada em cookie HttpOnly (seguro)

## 🐛 Troubleshooting

### Página não carrega dados

1. Verificar console do navegador (F12)
2. Verificar aba Network para erros de API
3. Certificar-se de que está autenticado
4. Tentar refresh (Ctrl+R ou Cmd+R)

### Formulário não envia

1. Verificar se todos os campos * estão preenchidos
2. Verificar console para erros JavaScript
3. Tentar fazer logout e login novamente

### Tabela está vazia

1. Confirmar que existem registros cadastrados
2. Tentar clicar no botão de refresh
3. Verificar se a API está retornando dados

## ⚙️ Mudanças Técnicas para Devs

### Backend

Arquivo modificado: `backend/app/routes/public_routes.py`

Novas rotas:
```python
@public_bp.get("/portal/equipe")  # Dashboard
@public_bp.get("/portal/equipe/clientes")  # Customers
@public_bp.get("/portal/equipe/colaboradores")  # Employees
# ... etc
```

Cada rota retorna o HTML da página correspondente.

### Frontend

Novos arquivos em `portal/`:
- `shared/portal.css` - Estilos compartilhados
- `shared/app.js` - Lógica global (não usado por enquanto)
- `team/*.html` - Páginas individuais

Cada página é independente e carrega seus próprios dados.

### Reuso de Código

Todas as páginas reutilizam:
- `portal.js` - Funções compartilhadas (request, logout, etc)
- `portal.css` - Estilos base (Bootstrap)
- `portal/shared/portal.css` - Estilos adicionais

## 📚 Próximas Melhorias

1. **Sidebar de navegação**: Menu fixo à esquerda em desktop
2. **SPA**: Navegação sem reload de página
3. **Cache**: Armazenar dados localmente
4. **Notificações**: Toast notifications para feedback
5. **Dark mode**: Tema escuro alternativo
6. **Paginação**: Para listas grandes
7. **Busca/Filtro**: Filtrar resultados na tabela
8. **Edição inline**: Editar dados sem ir para modal separado
9. **Exportar**: Exportar tabelas para CSV/PDF
10. **Testes**: Testes automatizados E2E

## 💡 Dicas de Uso

- Use `/portal/equipe` como ponto de entrada após login
- Todos os links de "logout" levam você de volta a `/acesso/equipe`
- Os dados são salvos no servidor (banco de dados PostgreSQL)
- Não há sincronização em tempo real entre abas abertas (por enquanto)
