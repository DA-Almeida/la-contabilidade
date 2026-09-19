/* Portal - Funções Compartilhadas */

const api = `${window.location.origin}/api`;
const storageKey = 'la_access_token';
const userKey = 'la_current_user';

function session() {
  try {
    return { user: JSON.parse(localStorage.getItem(userKey)) };
  } catch {
    return { user: null };
  }
}

function clearSession() {
  localStorage.removeItem(storageKey);
  localStorage.removeItem(userKey);
}

async function logout() {
  await fetch(`${api}/auth/logout`, { method: 'POST', credentials: 'same-origin' });
  clearSession();
  window.location.assign('/');
}

function showFeedback(element, message, isError = true) {
  element.textContent = message;
  element.className = `feedback ${isError ? 'error' : 'success'}`;
}

async function signIn(event, expectedRoles) {
  event.preventDefault();
  const form = event.target;
  if (!(form instanceof HTMLFormElement)) return;
  const feedback = form.querySelector('.feedback');
  const button = form.querySelector('button[type="submit"]');
  const payload = {
    email: String(form.email.value || '').trim(),
    password: String(form.password.value || '')
  };
  button.disabled = true;
  showFeedback(feedback, 'Entrando...', false);
  try {
    const response = await fetch(`${api}/auth/login`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Não foi possível entrar.');
    if (!expectedRoles.includes(result.user.role)) throw new Error('Esta conta não tem acesso a esta área.');
    localStorage.setItem(userKey, JSON.stringify(result.user));
    window.location.assign(expectedRoles.includes('cliente') ? '/portal/cliente' : '/portal/equipe');
  } catch (error) {
    showFeedback(feedback, error.message);
  } finally {
    button.disabled = false;
  }
}

async function request(path, options = {}) {
  const headers = { ...options.headers };
  if (!(options.body instanceof FormData)) headers['Content-Type'] = 'application/json';
  const response = await fetch(`${api}${path}`, { ...options, headers, credentials: 'same-origin' });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Não foi possível carregar os dados.');
  return data;
}

function escapeHtml(value = '') {
  const div = document.createElement('div');
  div.textContent = value;
  return div.innerHTML;
}

function formatDate(value) {
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(value));
}

function toPayload(form) {
  const data = Object.fromEntries(new FormData(form));
  Object.keys(data).forEach((key) => {
    if (data[key] === '') delete data[key];
  });
  if (data.user_id) data.user_id = Number(data.user_id);
  if (data.customer_id) data.customer_id = Number(data.customer_id);
  if (data.assignee_id) data.assignee_id = Number(data.assignee_id);
  if (data.employee_id) data.employee_id = Number(data.employee_id);
  if (data.owner_id) data.owner_id = Number(data.owner_id);
  return data;
}

function statusBadge(status) {
  const colors = {
    ativo: 'status-ativo',
    inativo: 'status-inativo',
    aberto: 'status-aberto',
    fechado: 'status-fechado',
    pendente: 'status-pendente',
    concluido: 'status-concluido'
  };
  return `<span class="badge ${colors[status] || 'bg-secondary'}">${status}</span>`;
}

function formatMoney(value) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
}

function customerNameById(id, users) {
  const user = users.find(u => u.id === id);
  return user ? user.name : 'Desconhecido';
}

/* Portal Initialization */
async function initializePortal({ roles, load }) {
  let user;
  try {
    user = (await request('/auth/me')).user;
    localStorage.setItem(userKey, JSON.stringify(user));
  } catch {
    user = null;
  }
  
  const loginView = document.getElementById('loginView');
  const appView = document.getElementById('appView');
  
  if (loginView) loginView.classList.toggle('d-none', Boolean(user));
  if (appView) appView.classList.toggle('d-none', !user);
  
  if (!user) return;
  if (!roles.includes(user.role)) {
    clearSession();
    window.location.reload();
    return;
  }
  
  document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.name);
  load();
}

/* Utility functions */
function toPayload(form) {
  const data = Object.fromEntries(new FormData(form));
  Object.keys(data).forEach((key) => {
    if (data[key] === '') delete data[key];
  });
  if (data.user_id) data.user_id = Number(data.user_id);
  if (data.customer_id) data.customer_id = Number(data.customer_id);
  if (data.assignee_id) data.assignee_id = Number(data.assignee_id);
  if (data.employee_id) data.employee_id = Number(data.employee_id);
  if (data.owner_id) data.owner_id = Number(data.owner_id);
  return data;
}
