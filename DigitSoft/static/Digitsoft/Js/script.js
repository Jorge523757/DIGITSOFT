// ========== MODO OSCURO / CLARO SOLO BOTÓN SUPERIOR ========== //
const themeToggle = document.getElementById('themeToggle');

function getSavedTheme() {
    return localStorage.getItem('theme') || 'light';
}

function saveTheme(theme) {
    localStorage.setItem('theme', theme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        const text = themeToggle.querySelector('span');
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
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = getSavedTheme();
    applyTheme(savedTheme);
});

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
        saveTheme(newTheme);
        themeToggle.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            themeToggle.style.transform = 'rotate(0deg)';
        }, 300);
    });
}

if (window.matchMedia) {
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    if (!localStorage.getItem('theme')) {
        applyTheme(systemPrefersDark.matches ? 'dark' : 'light');
    }
    systemPrefersDark.addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
}

document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'D') {
        if (themeToggle) themeToggle.click();
    }
});

// ========== BOTÓN BACK TO TOP ========== //
const backToTopButton = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
    if (backToTopButton) {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    }
});
if (backToTopButton) {
    backToTopButton.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ========== PRELOADER ========== //
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        preloader.style.opacity = '0';
        setTimeout(() => {
            preloader.style.display = 'none';
        }, 300);
    }
});

console.log('Digit Soft - Website loaded successfully ✓');

// ========== CARRITO DE COMPRAS ========== //
const carrito = {};
const agregarBtns = document.querySelectorAll('.agregar-carrito');
const verCarritoBtn = document.getElementById('verCarrito');
const carritoModal = document.getElementById('carritoModal');
const carritoLista = document.getElementById('carritoLista');
const cerrarCarritoBtn = document.getElementById('cerrarCarrito');

agregarBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const card = btn.closest('.producto-card');
        const nombre = card.getAttribute('data-producto');
        if (!carrito[nombre]) {
            carrito[nombre] = 1;
        } else {
            carrito[nombre]++;
        }
        mostrarCarrito();
    });
});

function mostrarCarrito() {
    if (!carritoLista || !carritoModal) return;
    carritoLista.innerHTML = '';
    Object.keys(carrito).forEach(producto => {
        const cantidad = carrito[producto];
        const li = document.createElement('li');
        li.textContent = `${producto}: ${cantidad} unidad(es)`;
        carritoLista.appendChild(li);
    });
    carritoModal.style.display = 'block';
}

if (verCarritoBtn) {
    verCarritoBtn.addEventListener('click', () => {
        mostrarCarrito();
    });
}
if (cerrarCarritoBtn) {
    cerrarCarritoBtn.addEventListener('click', () => {
        if (carritoModal) carritoModal.style.display = 'none';
    });
}

// ========== MENÚ LATERAL DESPLEGABLE ========== //
const sideMenuBtn = document.getElementById('sideMenuBtn');
const sideMenu = document.getElementById('sideMenu');
const closeSideMenu = document.getElementById('closeSideMenu');

if (sideMenuBtn && sideMenu && closeSideMenu) {
    sideMenuBtn.addEventListener('click', () => {
        sideMenu.classList.add('active');
    });
    closeSideMenu.addEventListener('click', () => {
        sideMenu.classList.remove('active');
    });
    document.addEventListener('click', (e) => {
        if (sideMenu.classList.contains('active') && !sideMenu.contains(e.target) && e.target !== sideMenuBtn) {
            sideMenu.classList.remove('active');
        }
    });
    sideMenu.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            sideMenu.classList.remove('active');
        });
    });
}

// ========== ANIMACIONES CON INTERSECTION OBSERVER ========== //
const observerOptions = { threshold: 0.1 };
const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
            obs.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.animate').forEach(el => {
    observer.observe(el);
});
