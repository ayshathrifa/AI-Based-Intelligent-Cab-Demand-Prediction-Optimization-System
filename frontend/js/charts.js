// charts.js — Dashboard chart initialization

const chartOptions = (yLabel) => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { labels: { color: '#e0e0e0' } } },
  scales: {
    x: { ticks: { color: '#a0a0b0' }, grid: { color: '#2a2a4a' } },
    y: { ticks: { color: '#a0a0b0' }, grid: { color: '#2a2a4a' }, title: { display: !!yLabel, text: yLabel, color: '#a0a0b0' } }
  }
});

document.addEventListener('DOMContentLoaded', () => {
  // Daily demand chart
  new Chart(document.getElementById('daily-chart').getContext('2d'), {
    type: 'line',
    data: {
      labels: Array.from({length: 24}, (_, i) => `${i}:00`),
      datasets: [{
        label: 'Demand',
        data: [5,3,2,2,4,12,45,85,82,55,40,48,52,45,38,42,60,88,94,80,65,50,35,18],
        borderColor: '#6c63ff',
        backgroundColor: 'rgba(108,99,255,0.15)',
        fill: true,
        tension: 0.4
      }]
    },
    options: chartOptions('Rides/hr')
  });

  // Weekly demand chart
  new Chart(document.getElementById('weekly-chart').getContext('2d'), {
    type: 'bar',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{
        label: 'Total Rides',
        data: [820, 850, 870, 900, 1100, 1350, 1200],
        backgroundColor: ['#6c63ff99','#6c63ff99','#6c63ff99','#6c63ff99','#f5a62399','#f44336cc','#f44336cc'],
        borderColor: ['#6c63ff','#6c63ff','#6c63ff','#6c63ff','#f5a623','#f44336','#f44336'],
        borderWidth: 2,
        borderRadius: 6
      }]
    },
    options: chartOptions()
  });

  // Zone chart
  new Chart(document.getElementById('zone-chart').getContext('2d'), {
    type: 'doughnut',
    data: {
      labels: ['Downtown', 'Airport', 'Suburbs', 'Mall', 'Hospital', 'Others'],
      datasets: [{
        data: [28, 18, 12, 15, 10, 17],
        backgroundColor: ['#6c63ff', '#f5a623', '#4caf50', '#a855f7', '#f44336', '#607d8b'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#e0e0e0' }, position: 'right' } }
    }
  });
});
