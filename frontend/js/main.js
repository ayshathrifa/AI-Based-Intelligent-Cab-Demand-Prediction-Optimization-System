// main.js — Dashboard data loader

async function loadDashboardStats() {
  try {
    const res = await fetch('/api/prediction/stats');
    const data = await res.json();
    document.getElementById('total-demand').textContent = data.total_demand || '1,284';
    document.getElementById('peak-hour').textContent = data.peak_hour || '6 PM';
    document.getElementById('active-drivers').textContent = data.active_drivers || '31';
    document.getElementById('top-zone').textContent = data.top_zone || 'Downtown';
  } catch {
    document.getElementById('total-demand').textContent = '1,284';
    document.getElementById('peak-hour').textContent = '6 PM';
    document.getElementById('active-drivers').textContent = '31';
    document.getElementById('top-zone').textContent = 'Downtown';
  }
}

async function loadRecentPredictions() {
  const mockData = [
    {time: '6:00 PM', zone: 'Downtown', demand: 87, status: 'High'},
    {time: '5:45 PM', zone: 'Airport', demand: 72, status: 'High'},
    {time: '5:30 PM', zone: 'Suburbs', demand: 34, status: 'Low'},
    {time: '5:15 PM', zone: 'Mall', demand: 65, status: 'Medium'},
    {time: '5:00 PM', zone: 'Hospital', demand: 48, status: 'Medium'},
  ];
  const badgeClass = {High: 'badge-danger', Medium: 'badge-warning', Low: 'badge-success'};
  document.getElementById('recent-table').innerHTML = mockData.map(r =>
    `<tr><td>${r.time}</td><td>${r.zone}</td><td>${r.demand}</td><td><span class="badge ${badgeClass[r.status]}">${r.status}</span></td></tr>`
  ).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  loadDashboardStats();
  loadRecentPredictions();
});
