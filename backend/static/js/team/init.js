/* Inicialização de páginas stub */

(async () => {
  try {
    const user = (await request('/auth/me')).user;
    document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.name);
  } catch (error) {
    logout();
  }
})();
