## 📁 Estrutura de Arquivos Estáticos (static/)

Este diretório contém todos os recursos estáticos do portal da equipe, organizados de forma profissional e escalável.

### Estrutura de Pastas

```
static/
├── css/
│   ├── portal.css        # Estilos base compartilhados
│   └── team.css          # Estilos específicos do portal de equipe
└── js/
    ├── portal.js         # Funções globais e utilitários
    └── team/
        ├── dashboard.js  # Lógica da página de dashboard
        ├── customers.js  # Lógica da página de clientes
        ├── employees.js  # Lógica da página de colaboradores
        ├── init.js       # Inicialização de páginas stub
        └── admin-init.js # Inicialização de páginas admin only
```

### 📄 Referência de Arquivos

#### CSS (static/css/)

| Arquivo | Propósito | Escopo |
|---------|----------|--------|
| **portal.css** | Estilos base do portal (navbar, layout base, responsividade) | Global |
| **team.css** | Estilos específicos do portal de equipe (cards, tabelas, badges) | Portal de Equipe |

#### JavaScript (static/js/)

| Arquivo | Propósito | Dependências |
|---------|----------|--------------|
| **portal.js** | Funções globais (API requests, auth, utilitários) | CDN Bootstrap |

#### JavaScript - Team (static/js/team/)

| Arquivo | Página | Propósito |
|---------|--------|----------|
| **dashboard.js** | `/portal/equipe` | Carrega 7 KPIs do dashboard |
| **customers.js** | `/portal/equipe/clientes` | CRUD de clientes |
| **employees.js** | `/portal/equipe/colaboradores` | CRUD de colaboradores |
| **init.js** | Stubs | Inicialização genérica |
| **admin-init.js** | `/portal/equipe/usuarios` | Inicialização com verificação admin |

### 🔗 Como Referenciar

#### No HTML

```html
<!-- CSS -->
<link rel="stylesheet" href="/static/css/portal.css">
<link rel="stylesheet" href="/static/css/team.css">

<!-- JavaScript -->
<script src="/static/js/portal.js"></script>
<script src="/static/js/team/dashboard.js"></script>
```

### 📝 Padrões

#### CSS

- ✅ Nomeação em kebab-case (`.page-header`)
- ✅ Responsividade mobile-first
- ✅ Reutilização via classes (`.badge`, `.status-ativo`)
- ✅ Organizado por componente

#### JavaScript

- ✅ Funções reutilizáveis globais em `portal.js`
- ✅ Lógica específica de página em arquivos separados
- ✅ Uso de `async/await` para operações assíncronas
- ✅ Tratamento de erro consistente
- ✅ Sem código embutido em HTML (JS externo)

### 🛡️ Segurança

✅ XSS Prevention: `escapeHtml()` em todos os dados dinâmicos
✅ CSRF Protection: Cookies HttpOnly (configurado no backend)
✅ Autenticação: Verificação em cada função crítica
✅ Role-based: Admin-only pages protegidas via `admin-init.js`

### ⚡ Performance

✅ Lazy loading: Dados carregam apenas quando necessário
✅ Minificação: CSS/JS compacto (pronto para produção)
✅ Cache: Cookies e localStorage para dados frequentes
✅ CDN: Bootstrap e Icons via CDN externo

### 📚 Adicionando Novas Páginas

1. **Criar arquivo HTML** em `portal/team/`
2. **Criar arquivo JS** em `static/js/team/` (se necessário)
3. **Referenciar** no HTML:
   ```html
   <link rel="stylesheet" href="/static/css/portal.css">
   <link rel="stylesheet" href="/static/css/team.css">
   <script src="/static/js/portal.js"></script>
   <script src="/static/js/team/sua-pagina.js"></script>
   ```

### ✅ Checklist

- ✅ Sem arquivos soltos na raiz
- ✅ Sem JS embutido em HTML
- ✅ Todos os .css em static/css/
- ✅ Todos os .js em static/js/team/
- ✅ Referências corretas com /static/
- ✅ Responsividade testada
- ✅ XSS prevention aplicada
- ✅ Pronto para produção

---

**Última atualização:** 18/09/2026
**Status:** ✅ Organização profissional concluída
