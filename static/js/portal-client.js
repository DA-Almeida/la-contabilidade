function clientTab(name, button){
  document.querySelectorAll('.client-section').forEach(section => section.classList.add('d-none'));
  document.getElementById(`client-${name}`).classList.remove('d-none');
  document.querySelectorAll('#clientTabs .nav-link').forEach(item => item.classList.remove('active'));
  button.classList.add('active');
}

async function loadClient(){
  try{
    const [{ documents }, { guides }, { obligations }, { tickets }] = await Promise.all([
      request('/documents'),
      request('/guides'),
      request('/fiscal-obligations'),
      request('/tickets'),
    ]);
    const count = document.getElementById('documentCount');
    if (count) count.textContent = documents.length;
    renderGuides(guides);
    renderObligations(obligations);
    renderClientTickets(tickets);

    const body = document.getElementById('documentsBody');
    if (!body) return;
    body.innerHTML = documents.length
      ? documents.map((document) => `<tr><td><strong>${escapeHtml(document.original_filename)}</strong><br><small class="text-secondary">${Math.ceil(document.size_bytes / 1024)} KB</small></td><td><span class="badge text-bg-light border">${escapeHtml(document.category)}</span></td><td>${formatDate(document.created_at)}</td><td class="text-end"><a class="btn btn-sm btn-outline-primary" href="/api/documents/${document.id}/download">Baixar</a></td></tr>`).join('')
      : '<tr><td colspan="4" class="text-secondary text-center py-4">Nenhum documento enviado.</td></tr>';
  } catch (error) {
    const body = document.getElementById('documentsBody');
    if (body) body.innerHTML = `<tr><td colspan="4" class="text-danger text-center py-4">${escapeHtml(error.message)}</td></tr>`;
  }
}

async function uploadClientDocument(event) {
  event.preventDefault();
  const form = event.target;
  const feedback = form.querySelector('.feedback');
  const button = form.querySelector('button');
  button.disabled = true;

  try {
    await request('/documents', { method: 'POST', body: new FormData(form) });
    form.reset();
    showFeedback(feedback, 'Documento enviado com sucesso.', false);
    await loadClient();
  } catch (error) {
    showFeedback(feedback, error.message);
  } finally {
    button.disabled = false;
  }
}

function renderGuides(guides) {
  const body = document.getElementById('guidesBody');
  if (!body) return;
  body.innerHTML = guides.length
    ? guides.map((guide) => `<tr><td>${escapeHtml(guide.title)}</td><td>${escapeHtml(guide.competence)}</td><td>${new Date(`${guide.due_date}T00:00`).toLocaleDateString('pt-BR')}</td><td>${formatMoney(guide.amount)}</td><td>${statusBadge(guide.status)}</td></tr>`).join('')
    : '<tr><td colspan="5" class="text-center text-secondary py-4">Nenhuma guia disponível.</td></tr>';
}

function renderObligations(items) {
  const list = document.getElementById('obligationsList');
  if (!list) return;
  list.innerHTML = items.length
    ? items.map((item) => `<div class="list-group-item d-flex justify-content-between gap-3 align-items-center"><div><strong>${escapeHtml(item.title)}</strong><div class="small text-secondary">${escapeHtml(item.competence)}${item.description ? ` · ${escapeHtml(item.description)}` : ''}</div></div><div class="text-end"><div class="small">${new Date(`${item.due_date}T00:00`).toLocaleDateString('pt-BR')}</div>${statusBadge(item.status)}</div></div>`).join('')
    : '<div class="list-group-item text-secondary text-center py-4">Nenhuma obrigação cadastrada.</div>';
}

function renderClientTickets(tickets) {
  const body = document.getElementById('ticketsBody');
  if (!body) return;
  body.innerHTML = tickets.length
    ? tickets.map((ticket) => `<tr><td>#${ticket.id}</td><td>${escapeHtml(ticket.subject)}<br><small class="text-secondary">${escapeHtml(ticket.category)}</small></td><td>${escapeHtml(ticket.priority)}</td><td>${statusBadge(ticket.status)}</td><td class="text-end"><button class="btn btn-sm btn-outline-primary" onclick="openClientTicket(${ticket.id})">Ver</button></td></tr>`).join('')
    : '<tr><td colspan="5" class="text-center text-secondary py-4">Nenhum ticket aberto.</td></tr>';
}

async function createClientTicket(event) {
  event.preventDefault();
  const form = event.target;
  const feedback = form.querySelector('.feedback');

  try {
    await request('/tickets', { method: 'POST', body: JSON.stringify(Object.fromEntries(new FormData(form))) });
    form.reset();
    showFeedback(feedback, 'Ticket aberto com sucesso.', false);
    loadClient();
  } catch (error) {
    showFeedback(feedback, error.message);
  }
}

async function openClientTicket(id) {
  try {
    const { ticket } = await request(`/tickets/${id}`);
    const detail = document.getElementById('ticketDetail');
    detail.classList.remove('d-none');
    detail.innerHTML = `<div class="d-flex justify-content-between"><h2 class="h6">Ticket #${ticket.id}: ${escapeHtml(ticket.subject)}</h2><button class="btn-close" onclick="document.getElementById('ticketDetail').classList.add('d-none')"></button></div><div class="vstack gap-2">${ticket.messages.map((message) => `<div class="rounded p-3 ${message.author_id === session().user.id ? 'bg-primary-subtle' : 'bg-body-tertiary'}"><div class="small fw-semibold">${escapeHtml(message.author_name)} · ${formatDate(message.created_at)}</div><div>${escapeHtml(message.body)}</div></div>`).join('')}</div>`;
  } catch (error) {
    alert(error.message);
  }
}
