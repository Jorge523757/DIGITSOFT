// ========== DASHBOARD JAVASCRIPT - COMPLETAMENTE ARREGLADO ========== //

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando Dashboard...');

    // Inicializar todas las funciones
    initializeTheme();
    initializeSidebar();
    initializeUserMenu();
    initializeAllButtons();
    initializeResponsive();
    initializeNotifications();

    // Inicializar después de cargar completamente
    window.addEventListener('load', function() {
        setTimeout(animateStats, 500);
        setTimeout(() => {
            showNotification('¡Bienvenido al Dashboard de Digit Soft!', 'success');
        }, 1000);
    });
});

// ========== GESTIÓN DE TEMA OSCURO/CLARO ========== //
function initializeTheme() {
    console.log('🎨 Inicializando sistema de temas...');

    // Obtener tema guardado o usar claro por defecto
    let currentTheme = localStorage.getItem('dashboard-theme') || 'light';

    // Aplicar tema inicial
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Configurar el botón
    const themeToggle = document.getElementById('themeToggleDashboard');
    if (themeToggle) {
        // Establecer icono inicial
        const icon = themeToggle.querySelector('.icon');
        if (icon) {
            icon.textContent = currentTheme === 'dark' ? '☀️' : '🌙';
        }

        // Agregar evento click
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            // Obtener tema actual y alternar
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = current === 'dark' ? 'light' : 'dark';

            console.log(`🔄 Cambiando de ${current} a ${newTheme}`);

            // Aplicar nuevo tema
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('dashboard-theme', newTheme);

            // Cambiar icono
            if (icon) {
                icon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
            }

            // Animación
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = 'rotate(0deg)';
            }, 300);

            // Notificación
            showNotification(`Tema cambiado a modo ${newTheme === 'dark' ? 'oscuro' : 'claro'}`, 'info');
        });

        console.log('✅ Botón de tema configurado correctamente');
    } else {
        console.error('❌ Botón de tema no encontrado');
    }
}

// ========== INICIALIZAR TODOS LOS BOTONES ========== //
function initializeAllButtons() {
    console.log('🔧 Inicializando todos los botones...');

    // Usar delegación de eventos para manejar todos los botones
    document.addEventListener('click', handleButtonClick);

    // Inicializar búsqueda en tiempo real
    document.addEventListener('input', handleSearchInput);

    console.log('✅ Todos los botones inicializados');
}

function handleButtonClick(e) {
    const target = e.target;
    const button = target.closest('button') || target.closest('a');

    if (!button) return;

    // Botones de accesos rápidos
    if (button.classList.contains('quick-access-item')) {
        e.preventDefault();
        const title = button.querySelector('h3')?.textContent || 'Módulo';
        showNotification(`Accediendo a ${title}...`, 'info');

        setTimeout(() => {
            const href = button.getAttribute('href');
            if (href && !href.includes('#')) {
                window.location.href = href;
            } else {
                showNotification(`${title} - Redirigiendo...`, 'success');
                // Mapear URLs correctas - ACTUALIZADO CON PRODUCTOS
                const urlMap = {
                    'Gestión de Clientes': '/administrador/clientes/',
                    'Órdenes de Servicio': '/administrador/orden-servicio/',
                    'Facturación': '/administrador/facturacion/',
                    'Inventario de Equipos': '/administrador/equipos/',
                    'Técnicos': '/administrador/tecnicos/',
                    'Ventas': '/administrador/ventas/',
                    'Gestión de Productos': '/administrador/productos/',
                    'Productos': '/administrador/productos/',
                    'Inventario de Productos': '/administrador/productos/',
                    'Catálogo de Productos': '/administrador/productos/',
                    'Gestión de Marcas': '/administrador/marcas/',
                    'Marcas': '/administrador/marcas/',
                    'Proveedores': '/administrador/proveedores/',
                    'Gestión de Proveedores': '/administrador/proveedores/',
                    'Compras': '/administrador/compras/',
                    'Gestión de Compras': '/administrador/compras/',
                    'Carritos': '/administrador/carritos/',
                    'Gestión de Carritos': '/administrador/carritos/',
                    'Servicios Técnicos': '/administrador/servicios-tecnicos/',
                    'Gestión de Servicios': '/administrador/servicios-tecnicos/',
                    'Garantías': '/administrador/garantias/',
                    'Gestión de Garantías': '/administrador/garantias/'
                };
                const url = urlMap[title];
                if (url) {
                    setTimeout(() => window.location.href = url, 500);
                } else {
                    console.warn(`URL no mapeada para: ${title}`);
                    showNotification(`Funcionalidad de ${title} en desarrollo`, 'warning');
                }
            }
        }, 1000);
        return;
    }

    // Botón agregar/nuevo
    if (button.classList.contains('btn-primary') || button.textContent.includes('Nuevo')) {
        e.preventDefault();
        const text = button.textContent.trim();
        showNotification(`${text} - Abriendo formulario...`, 'info');

        setTimeout(() => {
            if (confirm('¿Deseas abrir el formulario para agregar un nuevo elemento?')) {
                showNotification('Formulario abierto correctamente', 'success');
            }
        }, 500);
        return;
    }

    // Botón editar
    if (button.classList.contains('btn-edit') || button.textContent === '✏️') {
        e.preventDefault();
        const row = button.closest('tr, .card, .item');
        let itemName = 'elemento';

        if (row) {
            const nameElement = row.querySelector('td:nth-child(2), h3, .name');
            if (nameElement) {
                itemName = nameElement.textContent.trim();
            }
        }

        showNotification(`Editando: ${itemName}`, 'info');
        setTimeout(() => {
            if (confirm(`¿Deseas editar ${itemName}?`)) {
                showNotification(`Formulario de edición abierto para: ${itemName}`, 'success');
            }
        }, 500);
        return;
    }

    // Botón eliminar
    if (button.classList.contains('btn-delete') || button.textContent === '🗑️') {
        e.preventDefault();
        const itemName = button.dataset.name || button.getAttribute('data-name') || 'este elemento';

        if (confirm(`¿Estás seguro de que deseas eliminar ${itemName}?\n\nEsta acción no se puede deshacer.`)) {
            const row = button.closest('tr, .card, .item');
            if (row) {
                row.style.transition = 'all 0.3s ease';
                row.style.opacity = '0.5';
                row.style.transform = 'scale(0.95)';

                setTimeout(() => {
                    row.style.display = 'none';
                    showNotification(`${itemName} eliminado correctamente`, 'success');
                }, 300);
            } else {
                showNotification(`${itemName} eliminado correctamente`, 'success');
            }
        }
        return;
    }

    // Botón ver/visualizar
    if (button.textContent === '👁️' || button.title === 'Ver') {
        e.preventDefault();
        const row = button.closest('tr');
        let itemName = 'elemento';

        if (row) {
            const nameCell = row.querySelector('td:nth-child(2)');
            if (nameCell) {
                itemName = nameCell.textContent.trim();
            }
        }

        showNotification(`Visualizando detalles de: ${itemName}`, 'info');
        return;
    }

    // Botón imprimir
    if (button.textContent === '🖨️' || button.title === 'Imprimir') {
        e.preventDefault();
        showNotification('Generando documento...', 'info');

        setTimeout(() => {
            showNotification('Documento listo para imprimir', 'success');
            if (confirm('¿Deseas descargar el documento?')) {
                showNotification('Descarga iniciada', 'success');
            }
        }, 1500);
        return;
    }

    // Botón llamar
    if (button.textContent === '📞') {
        e.preventDefault();
        const card = button.closest('.technician-card');
        let techName = 'técnico';

        if (card) {
            const nameElement = card.querySelector('h3');
            if (nameElement) {
                techName = nameElement.textContent.trim();
            }
        }

        showNotification(`Llamando a ${techName}...`, 'info');
        setTimeout(() => {
            showNotification(`Conectado con ${techName}`, 'success');
        }, 2000);
        return;
    }

    // Botón filtros
    if (button.classList.contains('btn-icon') && (button.title === 'Filtros' || button.textContent === '🔍')) {
        e.preventDefault();
        showNotification('Panel de filtros abierto', 'info');
        openFiltersPanel();
        return;
    }
}

function handleSearchInput(e) {
    if (e.target.classList.contains('search-input')) {
        const searchTerm = e.target.value.toLowerCase().trim();
        searchInTable(searchTerm);

        if (searchTerm) {
            // Debounce para evitar muchas notificaciones
            clearTimeout(window.searchTimeout);
            window.searchTimeout = setTimeout(() => {
                const results = searchInTable(searchTerm);
                if (results > 0) {
                    showNotification(`${results} resultados encontrados`, 'success');
                }
            }, 800);
        }
    }
}

// ========== FUNCIONES DE UTILIDAD ========== //
function searchInTable(searchTerm) {
    const tables = document.querySelectorAll('.data-table');
    const cards = document.querySelectorAll('.product-card, .service-card, .brand-card, .technician-card');
    let foundResults = 0;

    // Buscar en tablas
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm) || searchTerm === '') {
                row.style.display = '';
                foundResults++;
            } else {
                row.style.display = 'none';
            }
        });
    });

    // Buscar en tarjetas
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(searchTerm) || searchTerm === '') {
            card.style.display = '';
            foundResults++;
        } else {
            card.style.display = 'none';
        }
    });

    if (searchTerm && foundResults === 0) {
        clearTimeout(window.searchTimeout);
        showNotification('No se encontraron resultados', 'warning');
    }

    return foundResults;
}

function openFiltersPanel() {
    // Remover panel existente si existe
    const existingPanel = document.getElementById('filtersPanel');
    if (existingPanel) {
        existingPanel.remove();
    }

    const filtersHtml = `
        <div id="filtersPanel" style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--card-bg, #fff);
            border: 1px solid var(--border-color, #ddd);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            z-index: 10000;
            min-width: 300px;
        ">
            <h3 style="color: var(--text-primary, #333); margin-bottom: 1rem;">Filtros de Búsqueda</h3>
            <div style="margin-bottom: 1rem;">
                <label style="color: var(--text-secondary, #666); display: block; margin-bottom: 0.5rem;">Estado:</label>
                <select style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color, #ddd); border-radius: 4px;">
                    <option value="">Todos</option>
                    <option value="activo">Activo</option>
                    <option value="pendiente">Pendiente</option>
                    <option value="completado">Completado</option>
                </select>
            </div>
            <div style="margin-bottom: 1rem;">
                <label style="color: var(--text-secondary, #666); display: block; margin-bottom: 0.5rem;">Fecha:</label>
                <input type="date" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color, #ddd); border-radius: 4px;">
            </div>
            <div style="display: flex; gap: 1rem; justify-content: flex-end;">
                <button onclick="closeFiltersPanel()" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color, #ddd); border-radius: 4px; background: #fff; cursor: pointer;">Cancelar</button>
                <button onclick="applyFilters()" style="padding: 0.5rem 1rem; border: none; border-radius: 4px; background: #2a7ae4; color: white; cursor: pointer;">Aplicar</button>
            </div>
        </div>
        <div id="filtersOverlay" onclick="closeFiltersPanel()" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 9999;
        "></div>
    `;

    document.body.insertAdjacentHTML('beforeend', filtersHtml);
}

function closeFiltersPanel() {
    const panel = document.getElementById('filtersPanel');
    const overlay = document.getElementById('filtersOverlay');
    if (panel) panel.remove();
    if (overlay) overlay.remove();
}

function applyFilters() {
    showNotification('Filtros aplicados correctamente', 'success');
    closeFiltersPanel();
}

// ========== SIDEBAR ========== //
function initializeSidebar() {
    console.log('📊 Inicializando sidebar...');
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const menuToggle = document.getElementById('menuToggle');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
        });
    }

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // Restaurar estado
    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    if (isCollapsed && sidebar) {
        sidebar.classList.add('collapsed');
    }

    // Cerrar sidebar en mobile al hacer click fuera
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && sidebar) {
            if (!sidebar.contains(e.target) && (!menuToggle || !menuToggle.contains(e.target))) {
                sidebar.classList.remove('active');
            }
        }
    });

    updateActiveNavigation();
    console.log('✅ Sidebar inicializado correctamente');
}

function updateActiveNavigation() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');

    navItems.forEach(item => {
        item.classList.remove('active');
        const href = item.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.includes(href))) {
            item.classList.add('active');
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

        document.addEventListener('click', function() {
            userDropdown.classList.remove('show');
        });
    }
}

// ========== RESPONSIVE ========== //
function initializeResponsive() {
    window.addEventListener('resize', function() {
        const sidebar = document.getElementById('sidebar');
        if (window.innerWidth > 768 && sidebar) {
            sidebar.classList.remove('active');
        }
    });
}

// ========== NOTIFICACIONES ========== //
function initializeNotifications() {
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
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }
}

function showNotification(message, type = 'info') {
    let container = document.getElementById('notification-container');
    if (!container) {
        initializeNotifications();
        container = document.getElementById('notification-container');
    }

    const notification = document.createElement('div');
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };

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
        pointer-events: auto;
        cursor: pointer;
        background: ${colors[type] || colors.info};
    `;

    notification.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: none; border: none; color: white; font-size: 18px; cursor: pointer; padding: 0;">
                ×
            </button>
        </div>
    `;

    container.appendChild(notification);

    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }, 5000);

    notification.addEventListener('click', function() {
        this.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (this.parentNode) {
                this.parentNode.removeChild(this);
            }
        }, 300);
    });
}

// ========== ANIMACIONES ========== //
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-info h3, .stat-number');

    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent.replace(/\D/g, '')) || 0;
        if (finalValue === 0) return;

        const duration = 2000;
        const startTime = Date.now();

        function updateCount() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = Math.floor(finalValue * easeOutQuart);

            if (stat.textContent.includes('+')) {
                stat.textContent = currentValue + '+';
            } else if (stat.textContent.includes('/')) {
                stat.textContent = currentValue + '/7';
            } else {
                stat.textContent = currentValue;
            }

            if (progress < 1) {
                requestAnimationFrame(updateCount);
            } else {
                if (stat.textContent.includes('+')) {
                    stat.textContent = finalValue + '+';
                } else if (stat.textContent.includes('/')) {
                    stat.textContent = finalValue + '/7';
                } else {
                    stat.textContent = finalValue;
                }
            }
        }

        stat.textContent = '0';
        updateCount();
    });
}

// ========== SHORTCUTS DE TECLADO ========== //
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const themeToggle = document.getElementById('themeToggleDashboard');
        if (themeToggle) themeToggle.click();
    }

    if (e.key === 'Escape') {
        closeFiltersPanel();
        document.querySelectorAll('.user-dropdown.show').forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    }
});

// ========== FUNCIONES GLOBALES ========== //
window.closeFiltersPanel = closeFiltersPanel;
window.applyFilters = applyFilters;
window.showNotification = showNotification;

// ========== UTILIDADES GLOBALES ========== //
window.dashboardUtils = {
    showNotification,
    animateStats,
    searchInTable,
    openFiltersPanel,
    closeFiltersPanel
};

console.log('🚀 Dashboard de Digit Soft cargado correctamente');
