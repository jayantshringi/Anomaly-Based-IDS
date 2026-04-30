const socket = io();

// UI Elements
const currentPpsEl = document.getElementById('current-pps');
const currentSizeEl = document.getElementById('current-size');
const anomalyCountEl = document.getElementById('anomaly-count');
const alertsContainer = document.getElementById('alerts-container');
const sidebar = document.getElementById('sidebar');

let anomalyCount = 0;

// Chart Setup
const ctx = document.getElementById('trafficChart').getContext('2d');
const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)');
gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

const chartConfig = {
    type: 'line',
    data: {
        labels: Array(60).fill(''),
        datasets: [{
            label: 'Packets/sec',
            data: Array(60).fill(0),
            borderColor: '#3b82f6',
            backgroundColor: gradient,
            borderWidth: 2,
            pointRadius: 0,
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 0
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)'
                },
                ticks: {
                    color: '#94a3b8',
                    font: { family: 'JetBrains Mono' }
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    display: false
                }
            }
        },
        plugins: {
            legend: { display: false }
        }
    }
};

const trafficChart = new Chart(ctx, chartConfig);

// Socket Listeners
socket.on('connect', () => {
    console.log('Connected to IDS server');
});

socket.on('traffic_update', (data) => {
    const pps = data.pps;
    const avgSize = data.avg_size;

    // Update Stats
    currentPpsEl.textContent = pps.toFixed(1);
    currentSizeEl.textContent = avgSize.toFixed(0) + ' B';

    // Update Chart
    const dataset = trafficChart.data.datasets[0].data;
    dataset.push(pps);
    dataset.shift();
    trafficChart.update();
});

socket.on('new_alert', (data) => {
    // Increment Count
    anomalyCount++;
    anomalyCountEl.textContent = anomalyCount;

    // Flash Sidebar
    sidebar.classList.add('alert-active');
    setTimeout(() => {
        sidebar.classList.remove('alert-active');
    }, 1000);

    // Remove "No alerts" text if present
    const noAlerts = document.querySelector('.no-alerts');
    if (noAlerts) noAlerts.remove();

    // Create Alert Element
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    
    const alertEl = document.createElement('div');
    alertEl.className = 'alert-item';
    alertEl.innerHTML = `
        <div class="alert-time">${timeStr}</div>
        <div class="alert-title">Traffic Spike Detected</div>
        <div class="alert-details">
            PPS: <span style="color: #fff">${data.pps.toFixed(1)}</span><br>
            Size: <span style="color: #fff">${data.avg_size.toFixed(0)} B</span><br>
            TCP: ${(data.tcp_ratio * 100).toFixed(0)}%
        </div>
    `;

    alertsContainer.prepend(alertEl);

    // Keep only last 50 alerts
    if (alertsContainer.children.length > 50) {
        alertsContainer.removeChild(alertsContainer.lastChild);
    }
});
