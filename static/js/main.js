document.addEventListener('DOMContentLoaded', function() {
    
    // Form Handling
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const loader = document.getElementById('loader');
            if (loader) {
                loader.classList.add('active');
            }
        });
    }

    // Quick Sample Buttons
    window.setValues = function(crypto, days) {
        const cryptoSelect = document.querySelector('select[name="crypto"]');
        const daysInput = document.querySelector('input[name="days"]');
        
        if (cryptoSelect && daysInput) {
            cryptoSelect.value = crypto;
            daysInput.value = days;
            
            // Visual feedback
            cryptoSelect.style.borderColor = 'var(--primary)';
            daysInput.style.borderColor = 'var(--primary)';
            setTimeout(() => {
                cryptoSelect.style.borderColor = '';
                daysInput.style.borderColor = '';
            }, 500);
        }
    };

    // Chart Initialization (if on results page)
    const ctx = document.getElementById('priceChart');
    if (ctx && window.chartData) {
        const data = window.chartData;
        
        // Create gradient
        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(0, 212, 255, 0.5)');
        gradient.addColorStop(1, 'rgba(0, 212, 255, 0.0)');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Historical Price',
                    data: data.historical,
                    borderColor: '#00d4ff',
                    backgroundColor: gradient,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'Prediction',
                    data: data.prediction_point, // Should be array with nulls and last point
                    borderColor: '#ff007a',
                    backgroundColor: '#ff007a',
                    borderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    borderDash: [5, 5]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
                plugins: {
                    legend: {
                        labels: { color: '#94a3b8' }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#94a3b8',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    }
});
