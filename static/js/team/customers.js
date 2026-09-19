/* Clientes - Lógica */

async function loadCustomers() {
  try {
    const response = await request('/operations/customers');
    const body = document.getElementById('customersBody');
    body.innerHTML = response.customers.length ? response.customers.map(c => `
      <tr>
        <td><strong>${escapeHtml(c.legal_name)}</strong></td>
        <td>${escapeHtml(c.tax_id)}</td>
        <td>${escapeHtml(c.tax_regime)}</td>
        <td>${formatMoney(c.monthly_fee || 0)}</td>
        <td>${statusBadge(c.status)}</td>
      </tr>
    `).join('') : '<tr><td colspan="5" class="text-center py-4 text-secondary">Nenhum cliente cadastrado.</td></tr>';
  } catch (error) {
    document.getElementById('customersBody').innerHTML = `<tr><td colspan="5" class="text-danger">Erro: ${error.message}</td></tr>`;
  }
}

async function submitCustomer(event) {
  event.preventDefault();
  const form = event.target;
  const feedback = form.querySelector('.feedback');
  try {
    const data = Object.fromEntries(new FormData(form));
    if (data.monthly_fee) data.monthly_fee = parseFloat(data.monthly_fee);
    await request('/operations/customers', { method: 'POST', body: JSON.stringify(data) });
    form.reset();
    showFeedback(feedback, 'Cliente cadastrado com sucesso.', false);
    await loadCustomers();
  } catch (error) {
    showFeedback(feedback, error.message);
  }
}

async function initCustomers() {
  try {
    const user = (await request('/auth/me')).user;
    document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.name);
    await loadCustomers();
  } catch (error) {
    logout();
  }
}

document.addEventListener('DOMContentLoaded', initCustomers);
