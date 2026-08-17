# Plano de Implantação — Funcionalidades do Layout

Este plano substitui os dados simulados do `exemplo_layout_menus_funcionalidades.html` por dados persistidos, APIs protegidas e telas Bootstrap. Nenhum módulo dependerá de arrays em JavaScript para dados de negócio.

## Diretrizes obrigatórias

- Portais em rotas protegidas (`/portal/equipe` e `/portal/cliente`), com JWT em cookie `HttpOnly` e autorização no servidor.
- Interface responsiva em Bootstrap 5, com componentes nativos para navegação, cards, tabelas, modais, formulários, alertas e offcanvas no celular.
- Regras de negócio em services Flask; controllers apenas coordenam requisição e resposta.
- PostgreSQL como fonte de verdade. Uploads ficam em colunas `BYTEA`/`LargeBinary`, com nome original, MIME type, tamanho, hash, proprietário e auditoria. Não haverá uploads no filesystem.
- Todas as mutações terão validação, autorização e registro de evento/auditoria.

## Fase 1 — Fundamento e identidade (concluída parcialmente)

- [x] Site institucional, leads persistidos, Flask, PostgreSQL e bootstrap inicial do schema.
- [x] Usuários, perfis `admin`, `colaborador` e `cliente`; login, logout e rotas de portal protegidas.
- [x] Painel inicial de equipe e gestão básica de acessos.
- [ ] Alembic/Flask-Migrate para alterações incrementais de schema.
- [ ] Logs estruturados, auditoria e configuração por ambiente.

## Fase 2 — Portal do cliente: documentos e atendimento

1. **Documentos e upload** — `documents`: upload múltiplo, categoria, competência, status, BLOB, download autorizado, documentos enviados e recebidos, pendências e checklist mensal.
2. **Guias e impostos** — `tax_guides`: competência, vencimento, valor, status e documento associado; visão de próximos vencimentos.
3. **Calendário fiscal** — `fiscal_obligations`: obrigação, prazo, competência, responsável e situação.
4. **Folha de pagamento** — `payroll_closings` e itens: período, funcionários, valores, prazo, eSocial e documentos pendentes.
5. **Tickets** — `tickets` e `ticket_messages`: abertura, prioridade, categoria, histórico, resposta, encerramento e reabertura. Cliente vê somente os próprios tickets.

## Fase 3 — Cadastro e operação interna

1. **Colaboradores** — dados profissionais, setor, cargo, CRC, admissão, status, perfil e produtividade.
2. **Clientes** — CNPJ/CPF, tipo, regime tributário, contatos, cidade, mensalidade, status e observações.
3. **Responsáveis por setor** — relacionamento cliente × setor × colaborador, com histórico de alteração.
4. **Tarefas/Kanban** — título, cliente, setor, responsável, prioridade, prazo e workflow `criado → análise → andamento → aguardando cliente → concluído`; toda transição validada e auditada.
5. **Agenda** — reuniões, visitas, treinamentos e prazos; filtros, responsáveis, clientes e conclusão/cancelamento.

## Fase 4 — Comercial e financeiro

1. **CRM** — leads de site e manuais, origem, serviço, valor estimado, estágio do funil e conversão em cliente.
2. **Financeiro** — receitas/despesas, categorias, forma de pagamento, anexos e exclusão lógica.
3. **Contas a pagar/receber** — vencimento, contraparte, baixa, atraso, saldo projetado e vínculo com cliente/fornecedor.
4. **Relatórios** — faturamento, inadimplência, produtividade, tarefas por situação, clientes por regime e exportação CSV/PDF.

## Fase 5 — Conformidade, alertas e publicação

1. **Validade de documentos** — emissão, vencimento, dias restantes e alertas de 30/15/7 dias e vencidos.
2. **Notificações** — central para tickets, tarefas, prazos, contas e documentos, com leitura e preferências.
3. **Whitelabel** — título, logotipo e informações institucionais em configurações administrativas.
4. **Qualidade** — testes de API por perfil, testes de upload/download BLOB, responsividade Bootstrap, acessibilidade, backup e política de retenção de arquivos.

## Ordem de entrega

1. Documentos BLOB e tela Bootstrap do cliente.
2. Tickets e guias/obrigações.
3. Clientes, colaboradores e tarefas/Kanban.
4. Agenda, CRM, financeiro e contas.
5. Validades, alertas, relatórios, auditoria e migrações formais.
