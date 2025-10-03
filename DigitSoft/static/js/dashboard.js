// ========== DASHBOARD JAVASCRIPT - COMPLETO ========== //

document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeSidebar();
    initializeUserMenu();
    initializeTableActions();
});

// ========== GESTIÓN DE TEMA OSCURO/CLARO ========== //
function initializeTheme() {
    const themeToggle = document.getElementById('themeToggleDashboard');

    // Obtener tema guardado o usar tema del sistema
    const savedTheme = localStorage.getItem('dashboard-theme') ||
                      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

    // Aplicar tema inicial
    applyTheme(savedTheme);

    // Listener para el botón de cambio de tema
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('dashboard-theme', newTheme);

            // Animación del botón
            themeToggle.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                themeToggle.style.transform = 'rotate(0deg)';
            }, 300);
        });
    }

    // Detectar cambios del tema del sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('dashboard-theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const themeToggle = document.getElementById('themeToggleDashboard');

    if (themeToggle) {
        const icon = themeToggle.querySelector('.icon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    // Actualizar meta theme-color para navegadores móviles
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) {
        metaThemeColor = document.createElement('meta');
        metaThemeColor.setAttribute('name', 'theme-color');
        document.head.appendChild(metaThemeColor);
    }
    metaThemeColor.setAttribute('content', theme === 'dark' ? '#1a1a1a' : '#ffffff');
}

// ========== GESTIÓN DEL SIDEBAR ========== //
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const menuToggle = document.getElementById('menuToggle');
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');

    // Toggle del sidebar (desktop)
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
        });
    }

    // Toggle del menú móvil
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Restaurar estado del sidebar
    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    if (isCollapsed && sidebar) {
        sidebar.classList.add('collapsed');
    }

    // Marcar elemento activo del menú
    const currentPath = window.location.pathname;
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });

    // Cerrar sidebar móvil al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        }
    });

    // Cerrar sidebar móvil al cambiar tamaño de ventana
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('show');
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

        // Cerrar dropdown al hacer clic fuera
        document.addEventListener('click', function() {
            userDropdown.classList.remove('show');
        });

        // Prevenir que se cierre al hacer clic dentro del dropdown
        userDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
}

// ========== ACCIONES DE TABLA ========== //
function initializeTableActions() {
    // Botones de editar
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const row = this.closest('tr');
            const id = row.cells[0].textContent;
            showNotification(`Editando elemento ${id}`, 'info');
            // Aquí puedes agregar la lógica para editar
        });
    });

    // Botones de eliminar
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const row = this.closest('tr');
            const id = row.cells[0].textContent;
            const name = row.cells[2] ? row.cells[2].textContent : 'este elemento';

            if (confirm(`¿Estás seguro de que quieres eliminar "${name}"?`)) {
                row.style.opacity = '0.5';
                showNotification(`Elemento ${id} eliminado`, 'success');
                setTimeout(() => {
                    row.remove();
                }, 500);
            }
        });
    });

    // Botones de ver
    document.querySelectorAll('.btn-view').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const row = this.closest('tr');
            const id = row.cells[0].textContent;
            showNotification(`Viendo detalles de ${id}`, 'info');
            // Aquí puedes agregar la lógica para ver detalles
        });
    });

    // Botón de nuevo elemento
    document.querySelectorAll('.btn-primary').forEach(btn => {
        if (btn.textContent.includes('Nuevo')) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                showNotification('Formulario de nuevo elemento', 'info');
                // Aquí puedes agregar la lógica para crear nuevo elemento
            });
        }
    });
}

// ========== SISTEMA DE NOTIFICACIONES ========== //
function showNotification(message, type = 'info') {
    // Crear contenedor de notificaciones si no existe
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(container);
    }

    // Crear notificación
    const notification = document.createElement('div');
    notification.style.cssText = `
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        word-wrap: break-word;
    `;

    // Colores según tipo
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };

    notification.style.backgroundColor = colors[type] || colors.info;
    notification.textContent = message;

    container.appendChild(notification);

    // Animación de entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// ========== UTILIDADES ========== //
// Formatear números como moneda
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

// Formatear fechas
function formatDate(dateString) {
    return new Intl.DateTimeFormat('es-CO', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).format(new Date(dateString));
}

// Validar formularios
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            field.style.borderColor = '';
        }
    });

    return isValid;
}

// Búsqueda en tablas
function setupTableSearch(tableId, searchInputId) {
    const table = document.getElementById(tableId);
    const searchInput = document.getElementById(searchInputId);

    if (table && searchInput) {
        searchInput.addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
}

// ========== ESTADÍSTICAS ANIMADAS ========== //
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-info h3');

    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        const duration = 2000; // 2 segundos
        const startTime = Date.now();

        function updateCount() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = Math.floor(finalValue * easeOutQuart);

            stat.textContent = currentValue;

            if (progress < 1) {
                requestAnimationFrame(updateCount);
            } else {
                stat.textContent = finalValue;
            }
        }

        updateCount();
    });
}

// ========== SHORTCUTS DE TECLADO ========== //
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K para cambiar tema
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const themeToggle = document.getElementById('themeToggleDashboard');
        if (themeToggle) themeToggle.click();
    }

    // Escape para cerrar modales y dropdowns
    if (e.key === 'Escape') {
        document.querySelectorAll('.user-dropdown.show').forEach(dropdown => {
            dropdown.classList.remove('show');
        });

        const sidebar = document.getElementById('sidebar');
        if (window.innerWidth <= 768 && sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
        }
    }

    // Ctrl/Cmd + / para toggle sidebar
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        const sidebarToggle = document.getElementById('sidebarToggle');
        if (sidebarToggle) sidebarToggle.click();
    }
});

// ========== INICIALIZACIÓN FINAL ========== //
// Animar estadísticas cuando la página se carga completamente
window.addEventListener('load', function() {
    setTimeout(animateStats, 500);
});

// Mostrar notificación de bienvenida
setTimeout(() => {
    showNotification('¡Bienvenido al Dashboard de Digit Soft!', 'success');
}, 1000);

console.log('🚀 Dashboard de Digit Soft cargado correctamente');
