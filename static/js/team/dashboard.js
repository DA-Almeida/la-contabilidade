/* Dashboard - Lógica */

async function initDashboard() {
  try {
    console.log('Dashboard initializing...');
    
    const authResponse = await request('/auth/me');
    console.log('Auth response:', authResponse);
    
    const user = authResponse.user;
    document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.name);

    const [
      leadsResponse,
      customersResponse,
      employeesResponse,
      tasksResponse,
      ticketsResponse,
      guidesResponse,
      obligationsResponse,
    ] = await Promise.all([
      request('/leads'),
      request('/operations/customers'),
      request('/operations/employees'),
      request('/operations/tasks'),
      request('/tickets'),
      request('/guides'),
      request('/fiscal-obligations'),
    ]);

    const stats = [
      { label: 'Leads', value: leadsResponse.leads.length, icon: 'bi-inbox' },
      { label: 'Clientes', value: customersResponse.customers.filter(c => c.status === 'ativo').length, icon: 'bi-people' },
      { label: 'Colaboradores', value: employeesResponse.employees.length, icon: 'bi-person-check' },
      { label: 'Tarafas abertas', value: tasksResponse.tasks.filter(t => t.status !== 'concluido').length, icon: 'bi-kanban' },
      { label: 'Tickets', value: ticketsResponse.tickets.filter(t => t.status === 'aberto').length, icon: 'bi-chat-dots' },
      { label: 'Guias pendentes', value: guidesResponse.guides.filter(g => g.status === 'pendente').length, icon: 'bi-book' },
      { label: 'Obrigações', value: obligationsResponse.obligations.filter(o => o.status === 'pendente').length, icon: 'bi-clipboard' },
    ];

    const container = document.getElementById('statsContainer');
    container.innerHTML = stats.map(s => `
      <div class="col-sm-6 col-lg-4">
        <div class="card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <div><p class="text-secondary small">${s.label}</p><p class="display-6 fw-bold mb-0">${s.value}</p></div>
              <i class="bi ${s.icon} text-primary" style="font-size:2rem;"></i>
            </div>
          </div>
        </div>
      </div>
    `).join('');
  } catch (error) {
    console.error('Dashboard error:', error);
    document.getElementById('statsContainer').innerHTML = `<div class="col-12"><div class="alert alert-danger">Erro: ${error.message}</div></div>`;
  }
}

document.addEventListener('DOMContentLoaded', initDashboard);
