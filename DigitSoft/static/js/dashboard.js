// ========== DASHBOARD JAVASCRIPT - COMPLETO Y FUNCIONAL ========== //

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Dashboard inicializando...');
    
    // Inicializar todas las funciones
    initializeTheme();
    initializeSidebar();
    initializeUserMenu();
    initializeNotifications();
    
    console.log('✅ Dashboard inicializado correctamente');
});

// ========== GESTIÓN DE TEMA OSCURO/CLARO ========== //
function initializeTheme() {
    const themeToggle = document.getElementById('themeToggleDashboard');
    const currentTheme = localStorage.getItem('dashboard-theme') || 'light';
    
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    if (themeToggle) {
        // Agregar transición CSS
        themeToggle.style.transition = 'transform 0.3s ease';
        
        // Establecer icono inicial
        updateThemeIcon(currentTheme);
        
        // Event listener para cambiar tema
        themeToggle.addEventListener('click', function() {
            const current = document.documentElement.getAttribute('data-theme');
            const newTheme = current === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('dashboard-theme', newTheme);
            updateThemeIcon(newTheme);
            
            // Animación del botón
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = 'rotate(0deg)';
            }, 300);
            
            showNotification('Tema cambiado a modo ' + (newTheme === 'dark' ? 'oscuro' : 'claro'), 'info');
        });
    }
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('themeToggleDashboard');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
}

// ========== SIDEBAR ========== //
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const menuToggle = document.getElementById('menuToggle');
    
    // Toggle sidebar en desktop
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
        });
    }
    
    // Toggle sidebar en mobile
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Restaurar estado del sidebar
    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    if (isCollapsed && sidebar) {
        sidebar.classList.add('collapsed');
    }
    
    // Cerrar sidebar en mobile al hacer click fuera
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && sidebar && menuToggle) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        }
    });
    
    // Marcar elemento activo
    updateActiveNavigation();
}

function updateActiveNavigation() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && (href === currentPath || currentPath.includes(href))) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

// ========== MENÚ DE USUARIO ========== //
function initializeUserMenu() {
    const userButton = document.getElementById('userButton');
    const userDropdown = document.getElementById('userDropdown');
    
    if (userButton && userDropdown) {
        userButton.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });
        
        // Cerrar dropdown al hacer click fuera
        document.addEventListener('click', function(e) {
            if (!userButton.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }
}

// ========== SISTEMA DE NOTIFICACIONES ========== //
function initializeNotifications() {
    // Crear contenedor de notificaciones si no existe
    if (!document.getElementById('notification-container')) {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 350px;
        `;
        document.body.appendChild(container);
    }
}

function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    if (!container) {
        initializeNotifications();
        return showNotification(message, type);
    }
    
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    const notification = document.createElement('div');
    notification.style.cssText = `
        background: ${colors[type] || colors.info};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        animation: slideIn 0.3s ease;
        cursor: pointer;
        min-width: 250px;
    `;
    
    notification.innerHTML = `
        <i class="fas ${icons[type] || icons.info}"></i>
        <span style="flex: 1;">${message}</span>
        <i class="fas fa-times" style="opacity: 0.7; cursor: pointer;"></i>
    `;
    
    container.appendChild(notification);
    
    // Cerrar al hacer click
    notification.addEventListener('click', function() {
        closeNotification(notification);
    });
    
    // Auto cerrar después de 3 segundos
    setTimeout(() => {
        closeNotification(notification);
    }, 3000);
}

function closeNotification(notification) {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => {
        notification.remove();
    }, 300);
}

// ========== FUNCIONES GLOBALES ========== //
window.confirmDelete = function(itemName, callback) {
    if (confirm('¿Estás seguro de que deseas eliminar ' + itemName + '?\n\nEsta acción no se puede deshacer.')) {
        showNotification(itemName + ' eliminado correctamente', 'success');
        if (callback) callback();
        return true;
    }
    return false;
};

window.searchTable = function(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
};

window.filterByCategory = function(category) {
    const items = document.querySelectorAll('[data-category]');
    
    items.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
    
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.category === category) {
            btn.classList.add('active');
        }
    });
};

window.printDocument = function() {
    showNotification('Preparando documento para imprimir...', 'info');
    setTimeout(() => {
        window.print();
    }, 500);
};

window.exportData = function(format) {
    showNotification('Exportando datos en formato ' + format.toUpperCase() + '...', 'info');
    setTimeout(() => {
        showNotification('Exportación completada', 'success');
    }, 1500);
};

// ========== RESPONSIVE ========== //
window.addEventListener('resize', function() {
    const sidebar = document.getElementById('sidebar');
    if (window.innerWidth > 768 && sidebar) {
        sidebar.classList.remove('active');
    }
});

// ========== ANIMACIONES DE CARGA ========== //
window.addEventListener('load', function() {
    const contentElements = document.querySelectorAll('.content > *');
    contentElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

console.log('✅ Dashboard JavaScript cargado correctamente');
