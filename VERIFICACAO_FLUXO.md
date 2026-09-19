# 🔍 VERIFICAÇÃO DO FLUXO - INSTRUÇÕES DE TESTE

## RESUMO DAS MUDANÇAS REALIZADAS

### ✅ Corrigidas as Referências de Arquivos Estáticos

1. **portal-admin.html** (Página de Login - Equipe)
   - ❌ Antes: `<link href="/portal.css">` → ✅ Agora: `<link href="/static/css/portal.css">`
   - ❌ Antes: `<script src="/portal.js">` → ✅ Agora: `<script src="/static/js/portal.js">`
   - ❌ Antes: `<script src="/portal-admin.js">` → ✅ Agora: `<script src="/static/js/portal-admin.js">`

2. **portal-cliente.html** (Página de Login - Cliente)
   - ❌ Antes: `<link href="/portal.css">` → ✅ Agora: `<link href="/static/css/portal.css">`
   - ❌ Antes: `<script src="/portal.js">` → ✅ Agora: `<script src="/static/js/portal.js">`
   - ❌ Antes: `<script src="/portal-client.js">` → ✅ Agora: `<script src="/static/js/portal-client.js">`

3. **portal/shared/layout.html** (Layout Compartilhado)
   - ❌ Antes: `<link href="/portal.css">` → ✅ Agora: `<link href="/static/css/portal.css">`
   - ❌ Antes: `<link href="/portal/shared/portal.css">` → ✅ Agora: `<link href="/static/css/team.css">`
   - ❌ Antes: `<script src="/portal.js">` → ✅ Agora: `<script src="/static/js/portal.js">`

### ✅ Criados/Copiados Arquivos Necessários

- ✅ `/static/js/portal-admin.js` - Copiado do `/portal-admin.js`
- ✅ `/static/js/portal-client.js` - Copiado do `/portal-client.js`
- ✅ `/static/js/portal.js` - Atualizado com `initializePortal()` e funções utilitárias

### ✅ Atualizado CSS

- ✅ `/static/css/portal.css` - Adicionados estilos para status badges, skeleton loaders, etc.

---

## 🧪 ROTEIRO DE TESTE (3 ETAPAS)

### ETAPA 1: Verificar Arquivo HTML (5 min)
```bash
# Terminal
curl -s http://localhost:5000/portal/equipe | grep -E 'dashboard\.js|portal\.js|portal\.css' | head -5
```

**Resultado Esperado:**
```html
<link rel="stylesheet" href="/static/css/portal.css">
<link rel="stylesheet" href="/static/css/team.css">
<script src="/static/js/portal.js"></script>
<script src="/static/js/team/dashboard.js"></script>
```

---

### ETAPA 2: Testar Login (10 min)

**Cenário:** Login na plataforma

1. **Abrir em novo navegador**
   - URL: `http://localhost:5000/acesso/equipe`

2. **Verificar se a página de login carrega**
   - ✅ Logo "L&A Contabilidade" visível
   - ✅ Form com campos "E-mail" e "Senha"
   - ✅ Botão "Entrar" funcional
   - ✅ Bootstrap CSS aplicado (estilos azuis, cards)

3. **Verificar no Console (F12)**
   - ✅ Sem erros 404 para `/static/css/portal.css`
   - ✅ Sem erros para `/static/js/portal.js`
   - ✅ Sem erros para `/static/js/portal-admin.js`

4. **Tentar login**
   - Email: `admin@exemplo.com` (ou seu email de admin)
   - Senha: sua senha
   - **Esperado:** Redireciona para `/portal/equipe`

---

### ETAPA 3: Testar Dashboard (15 min)

**Cenário:** Após login bem-sucedido

1. **Acessar Dashboard**
   - URL deve estar: `http://localhost:5000/portal/equipe`

2. **Verificar Estrutura**
   - ✅ Navbar azul com logo "L&A Contabilidade"
   - ✅ Texto "Olá, [seu nome]" na navbar
   - ✅ Botão "Sair" funcional
   - ✅ Título "Dashboard" visível
   - ✅ Subtítulo "Resumo da operação..."

3. **Verificar Carregamento de Dados (CRÍTICO)**
   - Abrir **Console (F12)** e verificar os logs:
     ```
     Dashboard initializing...
     Auth response: { user: { id: ..., name: "...", role: "..." } }
     ```
   - Se ver isso, tudo OK!

4. **Resultado Esperado (Final)**
   - ✅ Cards com números aparecem:
     - "Leads": X
     - "Clientes": X
     - "Colaboradores": X
     - "Tarefas abertas": X
     - "Tickets": X
     - "Guias pendentes": X
     - "Obrigações": X

---

## 🐛 POSSÍVEIS PROBLEMAS E SOLUÇÕES

### Problema 1: "Erro 404 - Não encontrado"
**Solução:**
```bash
# Verifi car se o servidor está rodando
lsof -ti:5000
# Se não houver output, iniciar:
cd /home/dcalmeida/Documentos/GitHub/la-contabilidade/backend
python run.py
```

### Problema 2: "Erro: Token de acesso inválido"
**Solução:**
1. Limpar localStorage: `localStorage.clear()` (F12 Console)
2. Fazer login novamente
3. Se persistir, verificar se o banco de dados tem admin

### Problema 3: "Cards vazios com Loading (Skeleton)"
**Ação:**
1. Abrir F12 Console
2. Ver os logs: `Dashboard initializing...`
3. Se houver erro, procure por: `Dashboard error: ...`
4. Relatar o erro

### Problema 4: "Erro 403 - Sem permissão"
**Solução:**
- Certifique-se que sua conta tem role `admin` ou `colaborador`
- Só `cliente` não tem acesso a `/portal/equipe`

---

## 📋 CHECKLIST FINAL

- [ ] Servidor rodando em `http://localhost:5000`
- [ ] Página de login carrega sem erros
- [ ] Login bem-sucedido redireciona para dashboard
- [ ] Dashboard mostra cards com dados
- [ ] Console (F12) não tem erros 404 ou 403
- [ ] Responsividade funciona (redimensione o navegador)
- [ ] Botão "Sair" funciona

---

## 📞 PRÓXIMAS AÇÕES SE HOUVER PROBLEMAS

Se você encontrar problemas:

1. **Compartilhe a saída do Console (F12)**
   - Screenshot ou cópia dos erros

2. **Verifique o terminal do servidor**
   - Pode ter erros do lado do backend

3. **Teste um endpoint isolado**
   ```bash
   curl -s http://localhost:5000/api/health
   # Deve retornar: {"status": "ok"}
   ```

---

## 🎉 SUCESSO!

Quando tudo funcionar, você terá:
- ✅ Arquivos estáticos em `/static/` (organizado)
- ✅ Dashboard carregando dados da API
- ✅ Sistema pronto para produção
- ✅ Base sólida para adicionar novas funcionalidades
