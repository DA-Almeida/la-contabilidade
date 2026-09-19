/* Kanban Tasks Management */

let currentUser = null;
let allTasks = [];
let allCustomers = [];
let allEmployees = [];
let allTeamUsers = [];
const DEPARTMENTS = ['Fiscal', 'Contábil', 'RH', 'Financeiro', 'Geral'];

(async () => {
  try {
    currentUser = (await request('/auth/me')).user;
    document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = currentUser.name);
    
    // Mostrar campo de privacidade apenas para admins/gerentes
    if (currentUser.role === 'admin' || currentUser.role === 'gerente') {
      document.getElementById('privateCheckContainer').style.display = 'block';
    }
    
    // Esconder botão de criar tarefa para não-admins/gerentes
    if (currentUser.role !== 'admin' && currentUser.role !== 'gerente' && currentUser.role !== 'colaborador') {
      document.getElementById('newTaskBtn').style.display = 'none';
    }
    
    // Carregar dados iniciais
    await loadKanbanData();
    await renderKanban();
    setupSortable();
  } catch (error) {
    console.error('Error:', error);
    logout();
  }
})();

async function loadKanbanData() {
  try {
    const [tasksRes, customersRes, employeesRes, usersRes] = await Promise.all([
      request('/operations/tasks'),
      request('/operations/customers'),
      request('/operations/employees'),
      request('/operations/team-users')
    ]);
    
    allTasks = tasksRes.tasks || [];
    allCustomers = customersRes.customers || [];
    allEmployees = employeesRes.employees || [];
    allTeamUsers = usersRes.users || [];
    
    populateSelects();
  } catch (error) {
    console.error('Error loading kanban data:', error);
  }
}

function populateSelects() {
  const deptSelect = document.getElementById('taskDepartment');
  const custSelect = document.getElementById('taskCustomer');
  const empSelect = document.getElementById('taskAssignee');
  
  deptSelect.innerHTML = '<option value="">Selecione um setor</option>' +
    DEPARTMENTS.map(d => `<option value="${d}">${d}</option>`).join('');
  
  custSelect.innerHTML = '<option value="">Nenhum cliente</option>' +
    allCustomers.map(c => `<option value="${c.id}">${c.legal_name}</option>`).join('');
  
  empSelect.innerHTML = '<option value="">Sem responsável</option>' +
    allEmployees.map(e => `<option value="${e.id}">${e.name}</option>`).join('');
}

async function renderKanban() {
  const statuses = ['criado', 'em_analise', 'em_andamento', 'aguardando_cliente', 'concluido'];
  
  statuses.forEach(status => {
    const lane = document.getElementById(`kanban-${status}`);
    if (lane) lane.innerHTML = '';
  });
  
  allTasks.forEach(task => {
    const lane = document.getElementById(`kanban-${task.status}`);
    if (!lane) return;
    
    const card = createTaskCard(task);
    lane.appendChild(card);
  });
  
  // Atualizar contadores
  statuses.forEach(status => {
    const count = allTasks.filter(t => t.status === status).length;
    document.getElementById(`count-${status}`).textContent = count;
  });
  
  // Mostrar mensagem vazia se nenhuma tarefa
  statuses.forEach(status => {
    const lane = document.getElementById(`kanban-${status}`);
    if (lane && lane.innerHTML === '') {
      lane.innerHTML = '<div class="empty-column">Sem tarefas</div>';
    }
  });
}

function createTaskCard(task) {
  const card = document.createElement('div');
  card.className = `kanban-card ${task.is_private ? 'private' : ''}`;
  card.draggable = true;
  card.dataset.taskId = task.id;
  card.onclick = () => showTaskDetails(task);
  
  const due = task.due_date ? new Date(`${task.due_date}T00:00`).toLocaleDateString('pt-BR') : '';
  
  card.innerHTML = `
    <div class="kanban-card-title">${escapeHtml(task.title)}</div>
    <div class="kanban-card-meta">
      <div><strong>${task.department}</strong></div>
      <div>Responsável: ${escapeHtml(task.assignee || 'N/A')}</div>
      <div>Cliente: ${escapeHtml(task.customer || 'N/A')}</div>
      ${due ? `<div>Prazo: ${due}</div>` : ''}
      <div>
        <span class="kanban-card-badge priority-${task.priority.toLowerCase()}">${task.priority}</span>
        ${task.is_private ? '<span class="kanban-card-badge" style="background:#dc3545;color:white;margin-left:0.25rem;">Privado</span>' : ''}
      </div>
    </div>
  `;
  
  return card;
}

function setupSortable() {
  const lanes = document.querySelectorAll('.kanban-lane');
  lanes.forEach(lane => {
    new Sortable(lane, {
      group: 'tasks',
      animation: 150,
      ghostClass: 'sortable-ghost',
      dragClass: 'sortable-drag',
      onEnd: async (evt) => {
        const taskId = parseInt(evt.item.dataset.taskId);
        const newStatus = evt.to.dataset.status;
        await moveTaskToStatus(taskId, newStatus);
      }
    });
  });
}

async function moveTaskToStatus(taskId, newStatus) {
  try {
    await request(`/operations/tasks/${taskId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status: newStatus })
    });
    await refreshKanban();
  } catch (error) {
    alert(`Erro ao mover tarefa: ${error.message}`);
    await refreshKanban();
  }
}

async function refreshKanban() {
  await loadKanbanData();
  await renderKanban();
}

function openNewTaskModal() {
  document.getElementById('newTaskForm').reset();
  new bootstrap.Modal(document.getElementById('newTaskModal')).show();
}

document.getElementById('newTaskForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const taskData = {
    title: document.getElementById('taskTitle').value,
    description: document.getElementById('taskDescription').value,
    department: document.getElementById('taskDepartment').value,
    priority: document.getElementById('taskPriority').value,
    customer_id: document.getElementById('taskCustomer').value || null,
    assignee_id: document.getElementById('taskAssignee').value || null,
    due_date: document.getElementById('taskDueDate').value || null,
    is_private: document.getElementById('taskIsPrivate').checked
  };
  
  try {
    await request('/operations/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData)
    });
    bootstrap.Modal.getInstance(document.getElementById('newTaskModal')).hide();
    await refreshKanban();
  } catch (error) {
    alert(`Erro ao criar tarefa: ${error.message}`);
  }
});

function showTaskDetails(task) {
  const modal = new bootstrap.Modal(document.getElementById('taskDetailsModal'));
  const content = document.getElementById('taskDetailsContent');
  const footer = document.getElementById('taskDetailsFooter');
  
  const due = task.due_date ? new Date(`${task.due_date}T00:00`).toLocaleDateString('pt-BR') : 'N/A';
  
  content.innerHTML = `
    <div class="mb-3">
      <h6>Título</h6>
      <p>${escapeHtml(task.title)}</p>
    </div>
    ${task.description ? `<div class="mb-3"><h6>Descrição</h6><p>${escapeHtml(task.description)}</p></div>` : ''}
    <div class="row">
      <div class="col-md-6 mb-3"><h6>Setor</h6><p>${escapeHtml(task.department)}</p></div>
      <div class="col-md-6 mb-3"><h6>Prioridade</h6><p><span class="kanban-card-badge priority-${task.priority.toLowerCase()}">${task.priority}</span></p></div>
    </div>
    <div class="row">
      <div class="col-md-6 mb-3"><h6>Cliente</h6><p>${escapeHtml(task.customer || 'N/A')}</p></div>
      <div class="col-md-6 mb-3"><h6>Responsável</h6><p>${escapeHtml(task.assignee || 'N/A')}</p></div>
    </div>
    <div class="mb-3"><h6>Status</h6><p>${task.status}</p></div>
    <div class="mb-3"><h6>Prazo</h6><p>${due}</p></div>
    ${task.is_private ? '<div class="alert alert-warning"><i class="bi bi-lock"></i> Esta tarefa é privada</div>' : ''}
  `;
  
  footer.innerHTML = `<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>`;
  modal.show();
}

function escapeHtml(text) {
  if (!text) return '';
  const map = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'};
  return text.replace(/[&<>"']/g, m => map[m]);
}
