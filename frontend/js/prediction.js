// prediction.js — Handles demand prediction form

const recommendations = {
  high: '🔴 High demand expected. Deploy maximum drivers to this zone immediately.',
  medium: '🟡 Moderate demand. Maintain current driver count with 2-3 on standby.',
  low: '🟢 Low demand. Drivers can be redistributed to higher-demand zones.'
};

document.getElementById('predict-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    hour: parseInt(document.getElementById('hour').value),
    day: parseInt(document.getElementById('day').value),
    zone: document.getElementById('zone').value,
    weather: document.getElementById('weather').value,
    temperature: parseFloat(document.getElementById('temperature').value) || 28,
    model: 'rf'
  };

  document.getElementById('placeholder-card').style.display = 'none';
  document.getElementById('result-section').style.display = 'none';
  document.getElementById('loading').style.display = 'block';

  try {
    const res = await fetch('/api/prediction/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    showResult(data.predicted_demand, payload);
  } catch {
    // Fallback demo prediction
    const base = 50;
    const hourBonus = (payload.hour >= 7 && payload.hour <= 9) || (payload.hour >= 17 && payload.hour <= 20) ? 35 : 0;
    const weatherBonus = {rain: 20, heavy_rain: 35, fog: 10, cloudy: 5, clear: 0}[payload.weather] || 0;
    const weekendBonus = payload.day >= 5 ? 15 : 0;
    showResult(base + hourBonus + weatherBonus + weekendBonus, payload);
  }
});

function showResult(demand, payload) {
  document.getElementById('loading').style.display = 'none';
  document.getElementById('result-section').style.display = 'block';
  document.getElementById('predicted-value').textContent = demand;

  const days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
  document.getElementById('details-table').innerHTML = `
    <tr><td style="color:var(--muted)">Hour</td><td>${payload.hour}:00</td></tr>
    <tr><td style="color:var(--muted)">Day</td><td>${days[payload.day]}</td></tr>
    <tr><td style="color:var(--muted)">Zone</td><td>${payload.zone}</td></tr>
    <tr><td style="color:var(--muted)">Weather</td><td>${payload.weather}</td></tr>
    <tr><td style="color:var(--muted)">Model</td><td>Random Forest 🌲</td></tr>`;

  const level = demand > 70 ? 'high' : demand > 40 ? 'medium' : 'low';
  document.getElementById('recommendation').textContent = recommendations[level];
}
