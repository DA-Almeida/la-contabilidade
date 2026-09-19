/* Inicialização de páginas admin */

(async () => {
  try {
    const user = (await request('/auth/me')).user;
    if (user.role !== 'admin') {
      window.location.href = '/portal/equipe';
      return;
    }
    document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.name);
  } catch (error) {
    logout();
  }
})();
