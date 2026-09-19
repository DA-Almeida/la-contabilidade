const api = `${window.location.origin}/api`;
const storageKey = 'la_access_token';
const userKey = 'la_current_user';

function session(){try{return {user:JSON.parse(localStorage.getItem(userKey))};}catch{return {user:null};}}
function clearSession(){localStorage.removeItem(storageKey);localStorage.removeItem(userKey);}
async function logout(){await fetch(`${api}/auth/logout`,{method:'POST',credentials:'same-origin'});clearSession();window.location.assign('/');}
function showFeedback(element,message,isError=true){element.textContent=message;element.className=`feedback ${isError?'error':'success'}`;}
async function signIn(event, expectedRoles){
  event.preventDefault();
  const form=event.target;
  if(!(form instanceof HTMLFormElement))return;
  const feedback=form.querySelector('.feedback');
  const button=form.querySelector('button[type="submit"]');
  const payload={
    email: String(form.email.value || '').trim(),
    password: String(form.password.value || '')
  };
  button.disabled=true;showFeedback(feedback,'Entrando...',false);
  try{
    const response=await fetch(`${api}/auth/login`,{
      method:'POST',
      credentials:'same-origin',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const result=await response.json();
    if(!response.ok)throw new Error(result.error||'Não foi possível entrar.');
    if(!expectedRoles.includes(result.user.role))throw new Error('Esta conta não tem acesso a esta área.');
    localStorage.setItem(userKey,JSON.stringify(result.user));
    window.location.assign(expectedRoles.includes('cliente')?'/portal/cliente':'/portal/equipe');
  }catch(error){showFeedback(feedback,error.message);}finally{button.disabled=false;}
}
async function request(path,options={}){
  const headers={...options.headers};
  if(!(options.body instanceof FormData))headers['Content-Type']='application/json';
  const response=await fetch(`${api}${path}`,{...options,headers,credentials:'same-origin'});
  const data=await response.json();
  if(!response.ok)throw new Error(data.error||'Não foi possível carregar os dados.');
  return data;
}
function escapeHtml(value=''){const div=document.createElement('div');div.textContent=value;return div.innerHTML;}
function formatDate(value){return new Intl.DateTimeFormat('pt-BR',{dateStyle:'short',timeStyle:'short'}).format(new Date(value));}
async function initializePortal({roles,load}){
  let user;
  try{user=(await request('/auth/me')).user;localStorage.setItem(userKey,JSON.stringify(user));}catch{user=null;}
  document.getElementById('loginView').classList.toggle('d-none',Boolean(user));
  document.getElementById('appView').classList.toggle('d-none',!user);
  if(!user)return;
  if(!roles.includes(user.role)){clearSession();window.location.reload();return;}
  document.querySelectorAll('[data-user-name]').forEach(el=>el.textContent=user.name);
  load();
}
async function loadAdmin(){
  try{
    const {user}=session();
    const [leadsResponse, customersResponse, employeesResponse, teamUsersResponse, tasksResponse, assignmentsResponse, ticketsResponse, guidesResponse, obligationsResponse, customerUsersResponse]=await Promise.all([
      request('/leads'),
      request('/operations/customers'),
      request('/operations/employees'),
      request('/operations/team-users'),
      request('/operations/tasks'),
      request('/operations/assignments?active_only=true'),
      request('/tickets'),
      request('/guides'),
      request('/fiscal-obligations'),
      request('/operations/customer-users'),
    ]);

    const leads=leadsResponse.leads;
    const customers=customersResponse.customers;
    const employees=employeesResponse.employees;
    const tasks=tasksResponse.tasks;
    const assignments=assignmentsResponse.assignments;
    const tickets=ticketsResponse.tickets;
    const guides=guidesResponse.guides;
    const obligations=obligationsResponse.obligations;
    const customerUsers=customerUsersResponse.users;

    document.getElementById('leadCount').textContent=leads.length;
    document.getElementById('customerCount').textContent=customers.filter(customer=>customer.status==='ativo').length;
    document.getElementById('employeeCount').textContent=employees.length;
    document.getElementById('taskOpenCount').textContent=tasks.filter(task=>task.status!=='concluido').length;
    document.getElementById('ticketOpenCount').textContent=tickets.filter(ticket=>ticket.status==='aberto').length;
    document.getElementById('guidePendingCount').textContent=guides.filter(guide=>guide.status==='pendente').length;
    document.getElementById('obligationPendingCount').textContent=obligations.filter(item=>item.status==='pendente').length;

    document.getElementById('leadsBody').innerHTML=leads.length?leads.map(lead=>`<tr><td>${escapeHtml(lead.name)}</td><td>${escapeHtml(lead.email)}</td><td>${escapeHtml(lead.company_type)}</td><td>${formatDate(lead.created_at)}</td></tr>`).join(''):'<tr><td colspan="4" class="empty">Nenhum contato recebido ainda.</td></tr>';

    renderCustomers(customers);
    renderEmployees(employees);
    renderTaskCustomers(customers);
    renderTaskAssignees(employees);
    renderAssignmentsCustomers(customers);
    renderAssignmentsEmployees(employees);
    renderAssignments(assignments);
    renderKanban(tasks);
    renderTeamUserOptions(teamUsersResponse.users, employees);
    renderCustomerUserOptions(customerUsers);
    renderTeamTickets(tickets, customerUsers);
    renderTeamGuides(guides, customerUsers);
    renderTeamObligations(obligations, customerUsers);

    if(user.role!=='admin'){
      document.querySelectorAll('.admin-only').forEach(el=>el.classList.add('d-none'));
      return;
    }

    const usersResponse=await request('/users');
    const users=usersResponse.users;
    document.getElementById('userCount').textContent=users.length;
    document.getElementById('usersBody').innerHTML=users.map(user=>`<tr><td>${escapeHtml(user.name)}</td><td>${escapeHtml(user.email)}</td><td><span class="badge">${escapeHtml(user.role)}</span></td></tr>`).join('');
  }catch(error){showFeedback(document.getElementById('adminFeedback'),error.message);}
}
async function createUser(event){
  event.preventDefault();const form=event.target,feedback=form.querySelector('.feedback');
  try{await request('/users',{method:'POST',body:JSON.stringify(Object.fromEntries(new FormData(form)))});form.reset();showFeedback(feedback,'Conta criada com sucesso.',false);loadAdmin();}catch(error){showFeedback(feedback,error.message);}
}

function toPayload(form){
  const data=Object.fromEntries(new FormData(form));
  Object.keys(data).forEach(key=>{if(data[key]==='')delete data[key];});
  if(data.user_id)data.user_id=Number(data.user_id);
  if(data.customer_id)data.customer_id=Number(data.customer_id);
  if(data.assignee_id)data.assignee_id=Number(data.assignee_id);
  if(data.employee_id)data.employee_id=Number(data.employee_id);
  if(data.owner_id)data.owner_id=Number(data.owner_id);
  return data;
}

async function createCustomer(event){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback');
  try{
    await request('/operations/customers',{method:'POST',body:JSON.stringify(toPayload(form))});
    form.reset();
    showFeedback(feedback,'Cliente cadastrado com sucesso.',false);
    await loadAdmin();
  }catch(error){showFeedback(feedback,error.message);}
}

async function createEmployee(event){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback');
  try{
    await request('/operations/employees',{method:'POST',body:JSON.stringify(toPayload(form))});
    form.reset();
    showFeedback(feedback,'Colaborador cadastrado com sucesso.',false);
    await loadAdmin();
  }catch(error){showFeedback(feedback,error.message);}
}

function renderCustomers(customers){
  const body=document.getElementById('customersBody');
  if(!body)return;
  body.innerHTML=customers.length?customers.map(customer=>`<tr><td><strong>${escapeHtml(customer.legal_name)}</strong></td><td>${escapeHtml(customer.tax_id)}</td><td>${escapeHtml(customer.tax_regime)}</td><td>${formatMoney(customer.monthly_fee||0)}</td><td>${statusBadge(customer.status)}</td></tr>`).join(''):'<tr><td colspan="5" class="text-secondary text-center py-4">Nenhum cliente cadastrado.</td></tr>';
}

function renderEmployees(employees){
  const body=document.getElementById('employeesBody');
  if(!body)return;
  body.innerHTML=employees.length?employees.map(employee=>`<tr><td><strong>${escapeHtml(employee.name)}</strong><br><small class="text-secondary">${escapeHtml(employee.email)}</small></td><td>${escapeHtml(employee.department)}</td><td>${escapeHtml(employee.job_title)}</td><td>${statusBadge(employee.employment_status)}</td></tr>`).join(''):'<tr><td colspan="4" class="text-secondary text-center py-4">Nenhum colaborador cadastrado.</td></tr>';
}

function renderTeamUserOptions(users, employees){
  const select=document.getElementById('teamUserSelect');
  if(!select)return;
  const usedUserIds=new Set(employees.map(employee=>employee.user_id));
  const available=users.filter(user=>!usedUserIds.has(user.id));
  const options=available.map(user=>`<option value="${user.id}">${escapeHtml(user.name)} (${escapeHtml(user.email)})</option>`).join('');
  select.innerHTML=`<option value="">Selecione um usuário</option>${options}`;
}

async function createTask(event){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback');
  try{
    await request('/operations/tasks',{method:'POST',body:JSON.stringify(toPayload(form))});
    form.reset();
    showFeedback(feedback,'Tarefa criada com sucesso.',false);
    await loadAdmin();
  }catch(error){showFeedback(feedback,error.message);}
}

function renderTaskCustomers(customers){
  const select=document.getElementById('taskCustomerSelect');
  if(!select)return;
  const options=customers.map(customer=>`<option value="${customer.id}">${escapeHtml(customer.legal_name)}</option>`).join('');
  select.innerHTML=`<option value="">Sem cliente vinculado</option>${options}`;
}

function renderTaskAssignees(employees){
  const select=document.getElementById('taskAssigneeSelect');
  if(!select)return;
  const options=employees.map(employee=>`<option value="${employee.id}">${escapeHtml(employee.name)} (${escapeHtml(employee.department)})</option>`).join('');
  select.innerHTML=`<option value="">Sem responsável</option>${options}`;
}

function statusLabel(status){
  const map={criado:'Criado',em_analise:'Análise',em_andamento:'Andamento',aguardando_cliente:'Aguardando cliente',concluido:'Concluído',aberto:'Aberto',respondido:'Respondido',resolvido:'Resolvido',pendente:'Pendente',pago:'Pago',ativo:'Ativo',inativo:'Inativo'};
  return map[status]||status;
}

function renderKanban(tasks){
  ['criado','em_analise','em_andamento','aguardando_cliente','concluido'].forEach(status=>{
    const col=document.getElementById(`kanban-${status}`);
    if(col)col.innerHTML='';
  });

  tasks.forEach(task=>{
    const col=document.getElementById(`kanban-${task.status}`);
    if(!col)return;
    const due=task.due_date?new Date(`${task.due_date}T00:00`).toLocaleDateString('pt-BR'):'Sem prazo';
    const nextOptions=(task.next_statuses||[]).map(next=>`<option value="${next}">${statusLabel(next)}</option>`).join('');
    const controls=task.next_statuses&&task.next_statuses.length?`<div class="d-flex gap-2 mt-2"><select class="form-select form-select-sm" id="next-${task.id}">${nextOptions}</select><button class="btn btn-sm btn-outline-primary" onclick="moveTask(${task.id})">Mover</button></div>`:'<div class="small text-success mt-2">Fluxo finalizado</div>';
    col.insertAdjacentHTML('beforeend',`<article class="border rounded bg-white p-2"><div class="fw-semibold">${escapeHtml(task.title)}</div><div class="small text-secondary">${escapeHtml(task.department)} · ${escapeHtml(task.priority)}</div><div class="small text-secondary">Cliente: ${escapeHtml(task.customer||'N/A')}</div><div class="small text-secondary">Resp.: ${escapeHtml(task.assignee||'N/A')}</div><div class="small text-secondary">Prazo: ${due}</div>${controls}</article>`);
  });

  ['criado','em_analise','em_andamento','aguardando_cliente','concluido'].forEach(status=>{
    const col=document.getElementById(`kanban-${status}`);
    if(col&&col.innerHTML==='')col.innerHTML='<div class="small text-secondary">Sem tarefas</div>';
  });
}

async function moveTask(taskId){
  const select=document.getElementById(`next-${taskId}`);
  if(!select||!select.value)return;
  try{
    await request(`/operations/tasks/${taskId}/status`,{method:'PATCH',body:JSON.stringify({status:select.value})});
    await loadAdmin();
  }catch(error){alert(error.message);}
}

function renderAssignmentsCustomers(customers){
  const select=document.getElementById('assignmentCustomerSelect');
  if(!select)return;
  const options=customers.map(customer=>`<option value="${customer.id}">${escapeHtml(customer.legal_name)}</option>`).join('');
  select.innerHTML=`<option value="">Selecione um cliente</option>${options}`;
}

function renderAssignmentsEmployees(employees){
  const select=document.getElementById('assignmentEmployeeSelect');
  if(!select)return;
  const options=employees.map(employee=>`<option value="${employee.id}">${escapeHtml(employee.name)} (${escapeHtml(employee.department)})</option>`).join('');
  select.innerHTML=`<option value="">Selecione um colaborador</option>${options}`;
}

function renderAssignments(assignments){
  const body=document.getElementById('assignmentsBody');
  if(!body)return;
  body.innerHTML=assignments.length?assignments.map(item=>`<tr><td>${escapeHtml(item.customer)}</td><td>${escapeHtml(item.department)}</td><td>${escapeHtml(item.employee)}</td><td>${formatDate(item.assigned_at)}</td></tr>`).join(''):'<tr><td colspan="4" class="text-secondary text-center py-4">Nenhuma atribuição ativa.</td></tr>';
}

async function createAssignment(event){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback');
  const data=toPayload(form);
  if(!data.customer_id){showFeedback(feedback,'Selecione um cliente.');return;}
  try{
    await request(`/operations/customers/${data.customer_id}/assignments`,{method:'POST',body:JSON.stringify({employee_id:data.employee_id,department:data.department})});
    form.reset();
    showFeedback(feedback,'Atribuição salva com sucesso.',false);
    await loadAdmin();
  }catch(error){showFeedback(feedback,error.message);}
}

function renderCustomerUserOptions(users){
  const options=users.map(user=>`<option value="${user.id}">${escapeHtml(user.name)} (${escapeHtml(user.email)})</option>`).join('');
  const guideSelect=document.getElementById('fiscalClientSelectGuide');
  const obligationSelect=document.getElementById('fiscalClientSelectObligation');
  if(guideSelect)guideSelect.innerHTML=`<option value="">Selecione um cliente</option>${options}`;
  if(obligationSelect)obligationSelect.innerHTML=`<option value="">Selecione um cliente</option>${options}`;
}

function customerNameById(ownerId, users){
  const found=users.find(user=>user.id===ownerId);
  return found?found.name:`Cliente #${ownerId}`;
}

function renderTeamTickets(tickets, users){
  const body=document.getElementById('teamTicketsBody');
  if(!body)return;
  body.innerHTML=tickets.length?tickets.map(ticket=>`<tr><td>#${ticket.id}</td><td>${escapeHtml(ticket.subject)}<br><small class="text-secondary">${escapeHtml(ticket.category)}</small></td><td>${escapeHtml(customerNameById(ticket.owner_id,users))}</td><td>${escapeHtml(ticket.priority)}</td><td>${statusBadge(ticket.status)}</td><td class="text-end"><button class="btn btn-sm btn-outline-primary" onclick="openTeamTicket(${ticket.id})">Ver</button></td></tr>`).join(''):'<tr><td colspan="6" class="text-secondary text-center py-4">Nenhum ticket encontrado.</td></tr>';
}

async function openTeamTicket(ticketId){
  try{
    const {ticket}=await request(`/tickets/${ticketId}`);
    const detail=document.getElementById('teamTicketDetail');
    const options=['aberto','respondido','resolvido'].map(status=>`<option value="${status}" ${ticket.status===status?'selected':''}>${statusLabel(status)}</option>`).join('');
    detail.classList.remove('d-none');
    detail.innerHTML=`<div class="d-flex justify-content-between align-items-start gap-2"><div><h3 class="h6 mb-1">Ticket #${ticket.id}: ${escapeHtml(ticket.subject)}</h3><div class="small text-secondary">Categoria: ${escapeHtml(ticket.category)} · Status: ${escapeHtml(ticket.status)}</div></div><button class="btn-close" onclick="document.getElementById('teamTicketDetail').classList.add('d-none')"></button></div><div class="vstack gap-2 mt-3">${ticket.messages.map(message=>`<div class="rounded p-2 bg-body-tertiary"><div class="small fw-semibold">${escapeHtml(message.author_name)} · ${formatDate(message.created_at)}</div><div>${escapeHtml(message.body)}</div></div>`).join('')}</div><form class="mt-3" onsubmit="replyTeamTicket(event,${ticket.id})"><label class="form-label">Responder</label><textarea class="form-control" name="message" rows="3" required></textarea><button class="btn btn-primary btn-sm mt-2">Enviar resposta</button><p class="feedback mt-2 mb-0" role="status"></p></form><div class="d-flex gap-2 align-items-end mt-3"><div><label class="form-label mb-1">Alterar status</label><select class="form-select form-select-sm" id="team-ticket-status-${ticket.id}">${options}</select></div><button class="btn btn-outline-primary btn-sm" onclick="updateTeamTicketStatus(${ticket.id})">Salvar status</button></div>`;
  }catch(error){alert(error.message);}
}

async function replyTeamTicket(event, ticketId){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback');
  try{
    await request(`/tickets/${ticketId}/messages`,{method:'POST',body:JSON.stringify(toPayload(form))});
    showFeedback(feedback,'Resposta enviada.',false);
    await openTeamTicket(ticketId);
    await loadAdmin();
  }catch(error){showFeedback(feedback,error.message);}
}

async function updateTeamTicketStatus(ticketId){
  const select=document.getElementById(`team-ticket-status-${ticketId}`);
  if(!select)return;
  try{
    await request(`/tickets/${ticketId}/status`,{method:'PATCH',body:JSON.stringify({status:select.value})});
    await openTeamTicket(ticketId);
    await loadAdmin();
  }catch(error){alert(error.message);}
}

async function createGuide(event){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback');
  try{
    await request('/guides',{method:'POST',body:JSON.stringify(toPayload(form))});
    form.reset();
    showFeedback(feedback,'Guia publicada com sucesso.',false);
    await loadAdmin();
  }catch(error){showFeedback(feedback,error.message);}
}

async function createObligation(event){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback');
  try{
    await request('/fiscal-obligations',{method:'POST',body:JSON.stringify(toPayload(form))});
    form.reset();
    showFeedback(feedback,'Obrigação publicada com sucesso.',false);
    await loadAdmin();
  }catch(error){showFeedback(feedback,error.message);}
}

function renderTeamGuides(guides, users){
  const list=document.getElementById('teamGuidesList');
  if(!list)return;
  if(!guides.length){list.innerHTML='Sem registros.';return;}
  list.innerHTML=guides.slice(0,5).map(guide=>`<div class="d-flex justify-content-between border-bottom py-1"><span>${escapeHtml(guide.title)} <span class="text-secondary">(${escapeHtml(customerNameById(guide.owner_id, users))})</span></span><span>${statusBadge(guide.status)}</span></div>`).join('');
}

function renderTeamObligations(obligations, users){
  const list=document.getElementById('teamObligationsList');
  if(!list)return;
  list.innerHTML=obligations.length?obligations.slice(0,8).map(item=>`<div class="list-group-item d-flex justify-content-between align-items-center"><div><strong>${escapeHtml(item.title)}</strong><div class="small text-secondary">${escapeHtml(customerNameById(item.owner_id, users))} · ${escapeHtml(item.competence)}</div></div>${statusBadge(item.status)}</div>`).join(''):'<div class="list-group-item text-secondary text-center py-4">Nenhuma obrigação publicada.</div>';
}
function clientTab(name, button){
  document.querySelectorAll('.client-section').forEach(section=>section.classList.add('d-none'));
  document.getElementById(`client-${name}`).classList.remove('d-none');
  document.querySelectorAll('#clientTabs .nav-link').forEach(item=>item.classList.remove('active'));
  button.classList.add('active');
}
async function loadClient(){
  try{
    const [{documents},{guides},{obligations},{tickets}]=await Promise.all([request('/documents'),request('/guides'),request('/fiscal-obligations'),request('/tickets')]);
    const count=document.getElementById('documentCount');if(count)count.textContent=documents.length;
    renderGuides(guides);renderObligations(obligations);renderClientTickets(tickets);
    const body=document.getElementById('documentsBody');if(!body)return;
    body.innerHTML=documents.length?documents.map(document=>`<tr><td><strong>${escapeHtml(document.original_filename)}</strong><br><small class="text-secondary">${Math.ceil(document.size_bytes/1024)} KB</small></td><td><span class="badge text-bg-light border">${escapeHtml(document.category)}</span></td><td>${formatDate(document.created_at)}</td><td class="text-end"><a class="btn btn-sm btn-outline-primary" href="/api/documents/${document.id}/download">Baixar</a></td></tr>`).join(''):'<tr><td colspan="4" class="text-secondary text-center py-4">Nenhum documento enviado.</td></tr>';
  }catch(error){const body=document.getElementById('documentsBody');if(body)body.innerHTML=`<tr><td colspan="4" class="text-danger text-center py-4">${escapeHtml(error.message)}</td></tr>`;}
}
async function uploadClientDocument(event){
  event.preventDefault();const form=event.target,feedback=form.querySelector('.feedback'),button=form.querySelector('button');button.disabled=true;
  try{await request('/documents',{method:'POST',body:new FormData(form)});form.reset();showFeedback(feedback,'Documento enviado com sucesso.',false);await loadClient();}catch(error){showFeedback(feedback,error.message);}finally{button.disabled=false;}
}
function statusBadge(status){const map={pendente:'text-bg-warning',pago:'text-bg-success',aberto:'text-bg-primary',respondido:'text-bg-info',resolvido:'text-bg-success',ativo:'text-bg-success',inativo:'text-bg-secondary',concluido:'text-bg-success',aguardando_cliente:'text-bg-warning',em_andamento:'text-bg-primary',em_analise:'text-bg-info'};return `<span class="badge ${map[status]||'text-bg-secondary'}">${escapeHtml(statusLabel(status))}</span>`;}
function formatMoney(value){return new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(value);}
function renderGuides(guides){const body=document.getElementById('guidesBody');if(!body)return;body.innerHTML=guides.length?guides.map(guide=>`<tr><td>${escapeHtml(guide.title)}</td><td>${escapeHtml(guide.competence)}</td><td>${new Date(`${guide.due_date}T00:00`).toLocaleDateString('pt-BR')}</td><td>${formatMoney(guide.amount)}</td><td>${statusBadge(guide.status)}</td></tr>`).join(''):'<tr><td colspan="5" class="text-center text-secondary py-4">Nenhuma guia disponível.</td></tr>';}
function renderObligations(items){const list=document.getElementById('obligationsList');if(!list)return;list.innerHTML=items.length?items.map(item=>`<div class="list-group-item d-flex justify-content-between gap-3 align-items-center"><div><strong>${escapeHtml(item.title)}</strong><div class="small text-secondary">${escapeHtml(item.competence)}${item.description?` · ${escapeHtml(item.description)}`:''}</div></div><div class="text-end"><div class="small">${new Date(`${item.due_date}T00:00`).toLocaleDateString('pt-BR')}</div>${statusBadge(item.status)}</div></div>`).join(''):'<div class="list-group-item text-secondary text-center py-4">Nenhuma obrigação cadastrada.</div>';}
function renderClientTickets(tickets){const body=document.getElementById('ticketsBody');if(!body)return;body.innerHTML=tickets.length?tickets.map(ticket=>`<tr><td>#${ticket.id}</td><td>${escapeHtml(ticket.subject)}<br><small class="text-secondary">${escapeHtml(ticket.category)}</small></td><td>${escapeHtml(ticket.priority)}</td><td>${statusBadge(ticket.status)}</td><td class="text-end"><button class="btn btn-sm btn-outline-primary" onclick="openClientTicket(${ticket.id})">Ver</button></td></tr>`).join(''):'<tr><td colspan="5" class="text-center text-secondary py-4">Nenhum ticket aberto.</td></tr>';}
async function createClientTicket(event){event.preventDefault();const form=event.target,feedback=form.querySelector('.feedback');try{await request('/tickets',{method:'POST',body:JSON.stringify(Object.fromEntries(new FormData(form)))});form.reset();showFeedback(feedback,'Ticket aberto com sucesso.',false);loadClient();}catch(error){showFeedback(feedback,error.message);}}
async function openClientTicket(id){try{const {ticket}=await request(`/tickets/${id}`);const detail=document.getElementById('ticketDetail');detail.classList.remove('d-none');detail.innerHTML=`<div class="d-flex justify-content-between"><h2 class="h6">Ticket #${ticket.id}: ${escapeHtml(ticket.subject)}</h2><button class="btn-close" onclick="document.getElementById('ticketDetail').classList.add('d-none')"></button></div><div class="vstack gap-2">${ticket.messages.map(message=>`<div class="rounded p-3 ${message.author_id===session().user.id?'bg-primary-subtle':'bg-body-tertiary'}"><div class="small fw-semibold">${escapeHtml(message.author_name)} · ${formatDate(message.created_at)}</div><div>${escapeHtml(message.body)}</div></div>`).join('')}</div>`;}catch(error){alert(error.message);}}
