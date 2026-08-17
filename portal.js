const api = `${window.location.origin}/api`;
const storageKey = 'la_access_token';
const userKey = 'la_current_user';

function session(){try{return {user:JSON.parse(localStorage.getItem(userKey))};}catch{return {user:null};}}
function clearSession(){localStorage.removeItem(storageKey);localStorage.removeItem(userKey);}
async function logout(){await fetch(`${api}/auth/logout`,{method:'POST'});clearSession();window.location.assign('/');}
function showFeedback(element,message,isError=true){element.textContent=message;element.className=`feedback ${isError?'error':'success'}`;}
async function signIn(event, expectedRoles){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback'),button=form.querySelector('button');
  button.disabled=true;showFeedback(feedback,'Entrando...',false);
  try{
    const response=await fetch(`${api}/auth/login`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
    const result=await response.json();
    if(!response.ok)throw new Error(result.error||'Não foi possível entrar.');
    if(!expectedRoles.includes(result.user.role))throw new Error('Esta conta não tem acesso a esta área.');
    localStorage.setItem(userKey,JSON.stringify(result.user));
    window.location.assign(expectedRoles.includes('cliente')?'/portal/cliente':'/portal/equipe');
  }catch(error){showFeedback(feedback,error.message);}finally{button.disabled=false;}
}
async function bootstrapAdmin(event){
  event.preventDefault();
  const form=event.target,feedback=form.querySelector('.feedback'),button=form.querySelector('button');
  button.disabled=true;showFeedback(feedback,'Criando acesso...',false);
  try{
    const response=await fetch(`${api}/auth/bootstrap`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
    const result=await response.json();
    if(!response.ok)throw new Error(result.error||'Não foi possível criar o administrador.');
    localStorage.setItem(userKey,JSON.stringify(result.user));
    window.location.assign('/portal/equipe');
  }catch(error){showFeedback(feedback,error.message);}finally{button.disabled=false;}
}
async function request(path,options={}){
  const headers={...options.headers};
  if(!(options.body instanceof FormData))headers['Content-Type']='application/json';
  const response=await fetch(`${api}${path}`,{...options,headers});
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
    const leadsResponse=await request('/leads');
    const leads=leadsResponse.leads;
    document.getElementById('leadCount').textContent=leads.length;
    document.getElementById('leadsBody').innerHTML=leads.length?leads.map(lead=>`<tr><td>${escapeHtml(lead.name)}</td><td>${escapeHtml(lead.email)}</td><td>${escapeHtml(lead.company_type)}</td><td>${formatDate(lead.created_at)}</td></tr>`).join(''):'<tr><td colspan="4" class="empty">Nenhum contato recebido ainda.</td></tr>';
    if(user.role!=='admin'){document.querySelectorAll('.admin-only').forEach(el=>el.classList.add('hidden'));return;}
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
function statusBadge(status){const map={pendente:'text-bg-warning',pago:'text-bg-success',aberto:'text-bg-primary',respondido:'text-bg-info',resolvido:'text-bg-success'};return `<span class="badge ${map[status]||'text-bg-secondary'}">${escapeHtml(status)}</span>`;}
function formatMoney(value){return new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(value);}
function renderGuides(guides){const body=document.getElementById('guidesBody');if(!body)return;body.innerHTML=guides.length?guides.map(guide=>`<tr><td>${escapeHtml(guide.title)}</td><td>${escapeHtml(guide.competence)}</td><td>${new Date(`${guide.due_date}T00:00`).toLocaleDateString('pt-BR')}</td><td>${formatMoney(guide.amount)}</td><td>${statusBadge(guide.status)}</td></tr>`).join(''):'<tr><td colspan="5" class="text-center text-secondary py-4">Nenhuma guia disponível.</td></tr>';}
function renderObligations(items){const list=document.getElementById('obligationsList');if(!list)return;list.innerHTML=items.length?items.map(item=>`<div class="list-group-item d-flex justify-content-between gap-3 align-items-center"><div><strong>${escapeHtml(item.title)}</strong><div class="small text-secondary">${escapeHtml(item.competence)}${item.description?` · ${escapeHtml(item.description)}`:''}</div></div><div class="text-end"><div class="small">${new Date(`${item.due_date}T00:00`).toLocaleDateString('pt-BR')}</div>${statusBadge(item.status)}</div></div>`).join(''):'<div class="list-group-item text-secondary text-center py-4">Nenhuma obrigação cadastrada.</div>';}
function renderClientTickets(tickets){const body=document.getElementById('ticketsBody');if(!body)return;body.innerHTML=tickets.length?tickets.map(ticket=>`<tr><td>#${ticket.id}</td><td>${escapeHtml(ticket.subject)}<br><small class="text-secondary">${escapeHtml(ticket.category)}</small></td><td>${escapeHtml(ticket.priority)}</td><td>${statusBadge(ticket.status)}</td><td class="text-end"><button class="btn btn-sm btn-outline-primary" onclick="openClientTicket(${ticket.id})">Ver</button></td></tr>`).join(''):'<tr><td colspan="5" class="text-center text-secondary py-4">Nenhum ticket aberto.</td></tr>';}
async function createClientTicket(event){event.preventDefault();const form=event.target,feedback=form.querySelector('.feedback');try{await request('/tickets',{method:'POST',body:JSON.stringify(Object.fromEntries(new FormData(form)))});form.reset();showFeedback(feedback,'Ticket aberto com sucesso.',false);loadClient();}catch(error){showFeedback(feedback,error.message);}}
async function openClientTicket(id){try{const {ticket}=await request(`/tickets/${id}`);const detail=document.getElementById('ticketDetail');detail.classList.remove('d-none');detail.innerHTML=`<div class="d-flex justify-content-between"><h2 class="h6">Ticket #${ticket.id}: ${escapeHtml(ticket.subject)}</h2><button class="btn-close" onclick="document.getElementById('ticketDetail').classList.add('d-none')"></button></div><div class="vstack gap-2">${ticket.messages.map(message=>`<div class="rounded p-3 ${message.author_id===session().user.id?'bg-primary-subtle':'bg-body-tertiary'}"><div class="small fw-semibold">${escapeHtml(message.author_name)} · ${formatDate(message.created_at)}</div><div>${escapeHtml(message.body)}</div></div>`).join('')}</div>`;}catch(error){alert(error.message);}}
