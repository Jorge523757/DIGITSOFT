// ========== GRÁFICOS DEL DASHBOARD ========== //

document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

function initializeCharts() {
    // Inicializar gráfico de ingresos
    initIncomeChart();
}

function initIncomeChart() {
    const canvas = document.getElementById('incomeChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Datos de ejemplo para el gráfico
    const data = {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        datasets: [{
            label: 'Ingresos 2025',
            data: [45000, 52000, 48000, 61000, 55000, 67000, 73000, 69000, 82000, 78000, 85000, 92000],
            borderColor: getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim(),
            backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim() + '20',
            fill: true,
            tension: 0.4
        }]
    };

    // Configuración del gráfico
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--card-bg').trim(),
                    titleColor: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim(),
                    bodyColor: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim(),
                    borderColor: getComputedStyle(document.documentElement).getPropertyValue('--border-color').trim(),
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border-color').trim()
                    },
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim(),
                        callback: function(value) {
                            return '$' + (value / 1000) + 'K';
                        }
                    }
                },
                x: {
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border-color').trim()
                    },
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim()
                    }
                }
            }
        }
    };

    // Crear el gráfico usando Chart.js si está disponible
    if (typeof Chart !== 'undefined') {
        new Chart(ctx, config);
    } else {
        // Fallback: crear un gráfico simple con canvas
        drawSimpleChart(ctx, data);
    }
}

// Función fallback para crear un gráfico simple sin Chart.js
function drawSimpleChart(ctx, data) {
    const canvas = ctx.canvas;
    const width = canvas.width;
    const height = canvas.height;

    // Limpiar canvas
    ctx.clearRect(0, 0, width, height);

    // Configuración
    const padding = 40;
    const chartWidth = width - (padding * 2);
    const chartHeight = height - (padding * 2);

    // Encontrar valores máximo y mínimo
    const values = data.datasets[0].data;
    const maxValue = Math.max(...values);
    const minValue = Math.min(...values);
    const valueRange = maxValue - minValue;

    // Estilos
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim() || '#2a7ae4';
    const textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim() || '#6c757d';
    const gridColor = getComputedStyle(document.documentElement).getPropertyValue('--border-color').trim() || '#dee2e6';

    // Dibujar grid
    ctx.strokeStyle = gridColor;
    ctx.lineWidth = 1;

    // Líneas horizontales
    for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(padding + chartWidth, y);
        ctx.stroke();
    }

    // Líneas verticales
    for (let i = 0; i <= data.labels.length - 1; i++) {
        const x = padding + (chartWidth / (data.labels.length - 1)) * i;
        ctx.beginPath();
        ctx.moveTo(x, padding);
        ctx.lineTo(x, padding + chartHeight);
        ctx.stroke();
    }

    // Dibujar línea de datos
    ctx.strokeStyle = primaryColor;
    ctx.lineWidth = 3;
    ctx.beginPath();

    values.forEach((value, index) => {
        const x = padding + (chartWidth / (values.length - 1)) * index;
        const y = padding + chartHeight - ((value - minValue) / valueRange) * chartHeight;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();

    // Dibujar puntos
    ctx.fillStyle = primaryColor;
    values.forEach((value, index) => {
        const x = padding + (chartWidth / (values.length - 1)) * index;
        const y = padding + chartHeight - ((value - minValue) / valueRange) * chartHeight;

        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fill();
    });

    // Añadir etiquetas
    ctx.fillStyle = textColor;
    ctx.font = '12px Inter, sans-serif';
    ctx.textAlign = 'center';

    // Etiquetas del eje X
    data.labels.forEach((label, index) => {
        const x = padding + (chartWidth / (data.labels.length - 1)) * index;
        ctx.fillText(label, x, height - 10);
    });

    // Etiquetas del eje Y
    ctx.textAlign = 'right';
    for (let i = 0; i <= 5; i++) {
        const value = minValue + (valueRange / 5) * (5 - i);
        const y = padding + (chartHeight / 5) * i + 5;
        ctx.fillText('$' + Math.round(value / 1000) + 'K', padding - 10, y);
    }
}

// Función para actualizar colores del gráfico cuando cambia el tema
function updateChartColors() {
    // Esta función se puede llamar cuando cambia el tema
    // para actualizar los colores de los gráficos existentes
    const charts = Chart.instances;
    if (charts) {
        Object.values(charts).forEach(chart => {
            if (chart && chart.options) {
                // Actualizar colores según el tema actual
                const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim();
                const textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim();
                const gridColor = getComputedStyle(document.documentElement).getPropertyValue('--border-color').trim();

                // Actualizar colores del dataset
                if (chart.data.datasets[0]) {
                    chart.data.datasets[0].borderColor = primaryColor;
                    chart.data.datasets[0].backgroundColor = primaryColor + '20';
                }

                // Actualizar colores de las escalas
                if (chart.options.scales) {
                    if (chart.options.scales.y) {
                        chart.options.scales.y.grid.color = gridColor;
                        chart.options.scales.y.ticks.color = textColor;
                    }
                    if (chart.options.scales.x) {
                        chart.options.scales.x.grid.color = gridColor;
                        chart.options.scales.x.ticks.color = textColor;
                    }
                }

                chart.update();
            }
        });
    }
}
