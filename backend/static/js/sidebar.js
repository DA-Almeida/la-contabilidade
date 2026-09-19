/**
 * Sidebar Menu System - Tree View com Expansão
 * Gerencia navegação com subitens, estado ativo e responsividade
 */

class SidebarMenu {
  constructor() {
    this.currentPage = null;
    this.expandedItems = new Set();
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.setupTreeView();
    this.setupMobileToggle();
    this.restoreExpandedState();
  }

  setupEventListeners() {
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', (e) => {
        if (!e.target.closest('.nav-toggle')) {
          e.preventDefault();
          const page = link.dataset.page;
          if (page) {
            this.setActivePage(link);
          }
        }
      });
    });

    document.querySelectorAll('.nav-toggle').forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        const parent = toggle.closest('.nav-item');
        const submenu = parent?.querySelector('.nav-submenu');
        
        if (submenu) {
          this.toggleSubmenu(submenu, toggle);
        }
      });
    });
  }

  setupTreeView() {
    document.querySelectorAll('.nav-item').forEach(item => {
      const submenu = item.querySelector('.nav-submenu');
      if (submenu) {
        item.classList.add('has-submenu');
      }
    });
  }

  toggleSubmenu(submenu, toggle) {
    const isShowing = submenu.classList.contains('show');
    
    if (isShowing) {
      submenu.classList.remove('show');
      toggle.classList.remove('expanded');
      const parent = submenu.closest('.nav-item');
      const mainLink = parent.querySelector('.nav-link:not(.nav-submenu .nav-link)');
      if (mainLink && mainLink.dataset.page) {
        this.expandedItems.delete(mainLink.dataset.page);
      }
    } else {
      submenu.classList.add('show');
      toggle.classList.add('expanded');
      const parent = submenu.closest('.nav-item');
      const mainLink = parent.querySelector('.nav-link:not(.nav-submenu .nav-link)');
      if (mainLink && mainLink.dataset.page) {
        this.expandedItems.add(mainLink.dataset.page);
      }
    }
    
    this.saveExpandedState();
  }

  setActivePage(link) {
    document.querySelectorAll('.nav-link').forEach(l => {
      l.classList.remove('active');
    });
    
    link.classList.add('active');
    
    const submenu = link.closest('.nav-submenu');
    if (submenu) {
      submenu.classList.add('show');
      const toggle = submenu.closest('.nav-item')?.querySelector('.nav-toggle');
      if (toggle) {
        toggle.classList.add('expanded');
      }
    }
    
    this.currentPage = link.dataset.page;
  }

  setupMobileToggle() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (!sidebarToggle) return;
    
    sidebarToggle.addEventListener('click', (e) => {
      e.preventDefault();
      const sidebar = document.getElementById('mainSidebar');
      if (sidebar) {
        sidebar.classList.toggle('show');
      }
    });
  }

  saveExpandedState() {
    const state = Array.from(this.expandedItems);
    localStorage.setItem('sidebar_expanded_state', JSON.stringify(state));
  }

  restoreExpandedState() {
    const saved = localStorage.getItem('sidebar_expanded_state');
    if (saved) {
      const state = JSON.parse(saved);
      state.forEach(page => {
        this.expandedItems.add(page);
        const link = document.querySelector(`[data-page="${page}"]`);
        if (link) {
          const parent = link.closest('.nav-item');
          const submenu = parent?.querySelector('.nav-submenu');
          const toggle = parent?.querySelector('.nav-toggle');
          
          if (submenu && toggle) {
            submenu.classList.add('show');
            toggle.classList.add('expanded');
          }
        }
      });
    }
  }

  syncWithMainNav(currentPage) {
    this.currentPage = currentPage;
    const activeLink = document.querySelector(`[data-page="${currentPage}"]`);
    if (activeLink) {
      this.setActivePage(activeLink);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.sidebarMenu = new SidebarMenu();
});
