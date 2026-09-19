/* Colaboradores - Lógica */

async function loadEmployees() {
  try {
    const [employeesResponse, usersResponse] = await Promise.all([
      request('/operations/employees'),
      request('/users')
    ]);

    const usedUserIds = new Set(employeesResponse.employees.map(e => e.user_id).filter(Boolean));
    const availableUsers = usersResponse.users.filter(u => !usedUserIds.has(u.id));
    document.getElementById('teamUserSelect').innerHTML = `<option value="">Selecione um usuário</option>${availableUsers.map(u => `<option value="${u.id}">${escapeHtml(u.name)}</option>`).join('')}`;

    const body = document.getElementById('employeesBody');
    body.innerHTML = employeesResponse.employees.length ? employeesResponse.employees.map(e => `
      <tr>
        <td><strong>${escapeHtml(e.name)}</strong><br><small class="text-secondary">${escapeHtml(e.email)}</small></td>
        <td>${escapeHtml(e.department)}</td>
        <td>${escapeHtml(e.job_title)}</td>
        <td>${statusBadge(e.employment_status)}</td>
      </tr>
    `).join('') : '<tr><td colspan="4" class="text-center py-4 text-secondary">Nenhum colaborador cadastrado.</td></tr>';
  } catch (error) {
    document.getElementById('employeesBody').innerHTML = `<tr><td colspan="4" class="text-danger">Erro: ${error.message}</td></tr>`;
  }
}

async function submitEmployee(event) {
  event.preventDefault();
  const form = event.target;
  const feedback = form.querySelector('.feedback');
  try {
    const data = Object.fromEntries(new FormData(form));
    if (data.user_id) data.user_id = parseInt(data.user_id);
    if (!data.user_id) delete data.user_id;
    await request('/operations/employees', { method: 'POST', body: JSON.stringify(data) });
    form.reset();
    showFeedback(feedback, 'Colaborador cadastrado com sucesso.', false);
    await loadEmployees();
  } catch (error) {
    showFeedback(feedback, error.message);
  }
}

async function initEmployees() {
  try {
    const user = (await request('/auth/me')).user;
    document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.name);
    await loadEmployees();
  } catch (error) {
    logout();
  }
}

document.addEventListener('DOMContentLoaded', initEmployees);
