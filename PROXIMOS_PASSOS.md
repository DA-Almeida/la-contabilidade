# 🔧 Próximos Passos - Implementação das Páginas

## 📋 Checklist de Implementação

- [ ] Tarefas (Kanban) - PRIORIDADE 🔥 ALTA
- [ ] Atribuições - PRIORIDADE 🟡 MÉDIA
- [ ] Tickets - PRIORIDADE 🟡 MÉDIA
- [ ] Guias - PRIORIDADE 🟡 MÉDIA
- [ ] Obrigações - PRIORIDADE 🟡 MÉDIA
- [ ] Usuários (admin) - PRIORIDADE 🟢 BAIXA

---

## 1. Tarafas (Kanban) - `/portal/equipe/tarefas`

### Especificação
- Colunas: Backlog, Em Andamento, Concluído, Arquivado
- Drag-and-drop entre colunas
- Formulário para criar tarefa
- Edição inline

### API
```
GET /api/operations/tasks
POST /api/operations/tasks
PATCH /api/operations/tasks/{id}/status
```

### Biblioteca
Usar SortableJS para drag-and-drop

---

## 2. Atribuições - `/portal/equipe/atribuicoes`

### Especificação
- Formulário: Cliente + Setor + Colaborador
- Tabela com atribuições ativas
- Opção de remover

### API
```
GET /api/operations/assignments
POST /api/operations/customers/{id}/assignments
```

---

## 3. Tickets - `/portal/equipe/tickets`

### Especificação
- Lista com status
- Detalhes ao clicar
- Formulário de resposta
- Mudança de status

### API
```
GET /api/tickets
POST /api/tickets/{id}/messages
PATCH /api/tickets/{id}/status
```

---

## 4. Guias - `/portal/equipe/guias`

### Especificação
- Formulário para publicar
- Lista de guias
- Filtro por status

### API
```
GET /api/guides
POST /api/guides
```

---

## 5. Obrigações - `/portal/equipe/obrigacoes`

### Especificação
- Formulário para criar
- Calendário com datas
- Indicador de vencimento

### API
```
GET /api/fiscal-obligations
POST /api/fiscal-obligations
```

---

## 6. Usuários - `/portal/equipe/usuarios` (Admin)

### Especificação
- CRUD de usuários
- Perfis (cliente/colaborador/admin)
- Reset de senha

### API
```
GET /api/users
POST /api/users
```

---

## 📝 Template Padrão

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Página - L&A Contabilidade</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/portal.css">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid px-lg-4">
      <a class="navbar-brand fw-bold" href="/">L&A Contabilidade</a>
      <span class="navbar-text ms-lg-auto me-lg-3">Olá, <span data-user-name></span></span>
      <button class="btn btn-outline-light btn-sm" onclick="logout()">Sair</button>
    </div>
  </nav>

  <div class="flex-grow-1 p-3 p-md-4 bg-light">
    <div class="page-header mb-4">
      <h1 class="page-title">Título</h1>
      <p class="page-subtitle">Descrição</p>
    </div>
    <!-- Seu conteúdo aqui -->
  </div>

  <script src="/portal.js"></script>
  <script>
    async function initPage() {
      try {
        const user = (await request('/auth/me')).user;
        document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.name);
        // Sua lógica aqui
      } catch (error) {
        logout();
      }
    }
    initPage();
  </script>
</body>
</html>
```

---

## ✅ Checklist por Página

- [ ] Navbar com logout
- [ ] Autenticação verificada
- [ ] Dados carregam
- [ ] Formulários funcionam
- [ ] Feedback visual
- [ ] Responsivo
- [ ] Sem erros console
- [ ] Sem XSS

---

## 🚀 Como Copiar do Código Antigo

O arquivo `portal-admin.js` contém as funções que você pode reutilizar:

- `renderKanban()` → Para Tarafas
- `renderAssignments()` → Para Atribuições
- `renderTeamTickets()` → Para Tickets
- `renderTeamGuides()` → Para Guias
- `renderTeamObligations()` → Para Obrigações
- `createUser()` → Para Usuários

Basta copiar a função e adaptar para a nova página.

---

Comece com **Tarafas** e siga o template! 🎯
