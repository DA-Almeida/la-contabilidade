#!/bin/bash
# GUIA DE TESTE - Refatoração da Área da Equipe

echo "================================"
echo "🧪 GUIA DE TESTE RÁPIDO"
echo "================================"
echo ""

echo "1️⃣ INICIAR SERVIDOR"
echo "cd /home/dcalmeida/Documentos/GitHub/la-contabilidade/backend"
echo "python run.py"
echo ""

echo "2️⃣ AGUARDAR INICIALIZAÇÃO"
echo "Esperar até aparecer: 'Running on http://0.0.0.0:5000'"
echo ""

echo "3️⃣ ABRIR NAVEGADOR"
echo "URL: http://localhost:5000/acesso/equipe"
echo ""

echo "4️⃣ LOGIN"
echo "Use suas credenciais de admin ou colaborador"
echo ""

echo "5️⃣ TESTAR DASHBOARD"
echo "URL: http://localhost:5000/portal/equipe"
echo "Verificar: 7 cards com dados carregando"
echo ""

echo "6️⃣ TESTAR CLIENTES"
echo "URL: http://localhost:5000/portal/equipe/clientes"
echo "✅ Verificar:"
echo "   - Formulário à esquerda"
echo "   - Tabela à direita"
echo "   - Tentar criar um novo cliente"
echo "   - Tabela atualiza automaticamente"
echo ""

echo "7️⃣ TESTAR COLABORADORES"
echo "URL: http://localhost:5000/portal/equipe/colaboradores"
echo "✅ Verificar:"
echo "   - Formulário à esquerda"
echo "   - Tabela à direita"
echo "   - Select de usuários carrega"
echo "   - Tentar criar um novo colaborador"
echo ""

echo "8️⃣ TESTAR RESPONSIVIDADE"
echo "F12 → Toggle device toolbar"
echo "✅ Verificar em iPhone/Android"
echo ""

echo "9️⃣ TESTAR ERRO (Logout)"
echo "Clique em 'Sair'"
echo "Deve voltar para: http://localhost:5000/acesso/equipe"
echo ""

echo "🔟 VERIFICAR CONSOLE"
echo "F12 → Console"
echo "✅ Não deve haver erros vermelhos"
echo ""

echo "================================"
echo "✅ TESTES CONCLUÍDOS!"
echo "================================"
