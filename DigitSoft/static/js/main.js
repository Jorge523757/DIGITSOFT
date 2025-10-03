// ========== MODO OSCURO / CLARO (ACTUALIZADO) ==========

const themeToggle = document.getElementById('themeToggle');
const themeToggleFloat = document.getElementById('themeToggleFloat');

// Función para obtener el tema guardado
function getSavedTheme() {
    return localStorage.getItem('theme') || 'light';
}

// Función para guardar el tema
function saveTheme(theme) {
    localStorage.setItem('theme', theme);
}

// Función para aplicar el tema
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);

    // Actualizar ambos botones
    const buttons = [themeToggle, themeToggleFloat];

    buttons.forEach(button => {
        if (button) {
            const icon = button.querySelector('i');
            const text = button.querySelector('span');

            if (theme === 'dark') {
                if (icon) icon.innerHTML = '☀️';
                if (text) text.textContent = 'Claro';
                document.body.classList.add('dark-mode');
            } else {
                if (icon) icon.innerHTML = '🌙';
                if (text) text.textContent = 'Oscuro';
                document.body.classList.remove('dark-mode');
            }
        }
    });
}

// Inicializar tema al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = getSavedTheme();
    applyTheme(savedTheme);
});

// Función para toggle del tema
function toggleTheme(button) {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    applyTheme(newTheme);
    saveTheme(newTheme);

    // Animación del botón
    if (button) {
        button.style.transform = button.id === 'themeToggleFloat'
            ? 'translateY(-50%) rotate(360deg)'
            : 'rotate(360deg)';

        setTimeout(() => {
            button.style.transform = button.id === 'themeToggleFloat'
                ? 'translateY(-50%) rotate(0deg)'
                : 'rotate(0deg)';
        }, 300);
    }
}

// Event listeners para ambos botones
if (themeToggle) {
    themeToggle.addEventListener('click', () => toggleTheme(themeToggle));
}

if (themeToggleFloat) {
    themeToggleFloat.addEventListener('click', () => toggleTheme(themeToggleFloat));
}

// Detectar preferencia del sistema (opcional)
if (window.matchMedia) {
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)');

    // Solo aplicar si no hay preferencia guardada
    if (!localStorage.getItem('theme')) {
        applyTheme(systemPrefersDark.matches ? 'dark' : 'light');
    }

    // Escuchar cambios en la preferencia del sistema
    systemPrefersDark.addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
}

// Atajo de teclado para cambiar tema (Ctrl + Shift + D)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'D') {
        toggleTheme(themeToggle || themeToggleFloat);
    }
});

console.log('Digit Soft - Theme system loaded ✓');