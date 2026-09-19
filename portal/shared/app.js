/**
 * Portal App - Core Application Module
 * Gerencia autenticação, navegação e estado global da aplicação
 */

class PortalApp {
  constructor() {
    this.currentUser = null;
    this.currentPage = null;
    this.modules = {};
    this.init();
  }

  async init() {
    try {
      // Carregar usuário autenticado
      const authResponse = await request('/auth/me');
      this.currentUser = authResponse.user;
      localStorage.setItem('la_current_user', JSON.stringify(this.currentUser));

      // Renderizar sidebar baseado no role
      this.renderSidebar();
      
      // Configurar navegação
      this.setupNavigation();
      
      // Carregar página inicial
      const currentPath = window.location.pathname;
      const page = this.getPageFromPath(currentPath) || 'dashboard';
      this.loadPage(page);

      // Atualizar nome do usuário
      document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = this.currentUser.name);

    } catch (error) {
      clearSession();
      window.location.assign('/acesso/equipe');
    }
  }

  renderSidebar() {
    // Mostrar seção admin-only apenas para admins
    if (this.currentUser.role === 'admin') {
      document.querySelectorAll('.admin-only').forEach(el => el.style.display = '');
    }
  }

  setupNavigation() {
    // Interceptar cliques em links de navegação
    document.querySelectorAll('.nav-item-link').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = link.dataset.page;
        this.loadPage(page);
      });
    });

    // Toggle sidebar em mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', () => {
        const sidebar = document.getElementById('mainSidebar');
        sidebar.classList.toggle('show');
      });
    }

    // Fechar sidebar ao clicar em um link (mobile)
    if (window.innerWidth < 768) {
      document.querySelectorAll('.nav-item-link').forEach(link => {
        link.addEventListener('click', () => {
          document.getElementById('mainSidebar').classList.remove('show');
        });
      });
    }
  }

  getPageFromPath(path) {
    const pathMap = {
      '/portal/equipe': 'dashboard',
      '/portal/equipe/clientes': 'customers',
      '/portal/equipe/colaboradores': 'employees',
      '/portal/equipe/tarefas': 'tasks',
      '/portal/equipe/atribuicoes': 'assignments',
      '/portal/equipe/tickets': 'tickets',
      '/portal/equipe/guias': 'guides',
      '/portal/equipe/obrigacoes': 'obligations',
      '/portal/equipe/usuarios': 'users',
    };
    return pathMap[path];
  }

  async loadPage(page) {
    try {
      // Marcar link como ativo
      document.querySelectorAll('.nav-item-link').forEach(link => {
        link.classList.toggle('active', link.dataset.page === page);
      });

      // Carregar módulo se não estiver em cache
      if (!this.modules[page] && typeof window[`load${this.capitalize(page)}`] === 'function') {
        this.currentPage = page;
        await window[`load${this.capitalize(page)}`]();
      } else if (this.modules[page]) {
        this.currentPage = page;
        this.modules[page].render();
      }

      // Atualizar URL sem recarregar
      const pathMap = {
        'dashboard': '/portal/equipe',
        'customers': '/portal/equipe/clientes',
        'employees': '/portal/equipe/colaboradores',
        'tasks': '/portal/equipe/tarefas',
        'assignments': '/portal/equipe/atribuicoes',
        'tickets': '/portal/equipe/tickets',
        'guides': '/portal/equipe/guias',
        'obligations': '/portal/equipe/obrigacoes',
        'users': '/portal/equipe/usuarios',
      };
      window.history.pushState({}, '', pathMap[page]);
    } catch (error) {
      console.error(`Erro ao carregar página ${page}:`, error);
      showFeedback(document.querySelector('[role="status"]'), `Erro ao carregar página: ${error.message}`);
    }
  }

  capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).replace(/([A-Z])/g, '$1');
  }

  logout() {
    logout();
  }

  registerModule(name, module) {
    this.modules[name] = module;
  }
}

// Inicializar app global
const portalApp = new PortalApp();
window.portalApp = portalApp;
