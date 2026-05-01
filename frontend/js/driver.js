// driver.js — Driver allocation logic

const ZONES = ['downtown', 'airport', 'suburbs', 'mall', 'hospital', 'university', 'station', 'business_park'];

const suggestions = [
  {zone: 'downtown',  label: 'Downtown',        current: 3, recommended: 8, reason: 'Evening peak — 87 rides/hr predicted'},
  {zone: 'station',   label: 'Railway Station',  current: 2, recommended: 6, reason: 'High consistent demand — 91 rides/hr'},
  {zone: 'airport',   label: 'Airport',          current: 4, recommended: 6, reason: 'Flight arrivals at 6 PM'},
  {zone: 'suburbs',   label: 'Suburbs',          current: 5, recommended: 2, reason: 'Low demand — redeploy to hotspots'},
];

let allDrivers = [];

function renderSuggestions() {
  document.getElementById('suggestions-list').innerHTML = suggestions.map(s => `
    <div style="padding:12px 0;border-bottom:1px solid #2a2a4a">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <strong>${s.label}</strong>
        <span style="color:var(--primary)">${s.current} → ${s.recommended} drivers</span>
      </div>
      <p style="color:var(--muted);font-size:0.82rem;margin-top:4px">${s.reason}</p>
    </div>`).join('');
}

function renderDriverTable(drivers) {
  const badgeClass = {Active: 'badge-success', Idle: 'badge-warning', Offline: 'badge-danger'};
  const zoneOptions = ZONES.map(z => `<option value="${z}">${z.charAt(0).toUpperCase()+z.slice(1)}</option>`).join('');
  document.getElementById('driver-table').innerHTML = drivers.map(d => `
    <tr>
      <td><div style="display:flex;align-items:center;gap:10px">
        <div class="driver-avatar" style="width:36px;height:36px;font-size:1rem">🚗</div>
        <div>
          <div style="font-weight:600">${d.name}</div>
          <div style="font-size:0.78rem;color:var(--muted)">${d.email}</div>
        </div>
      </div></td>
      <td>${d.zone.charAt(0).toUpperCase()+d.zone.slice(1)}</td>
      <td><span class="badge ${badgeClass[d.status] || 'badge-warning'}">${d.status}</span></td>
      <td>${d.rides_today}</td>
      <td>
        <select id="zone-select-${d.id}" style="padding:4px 8px;background:var(--darker);border:1px solid #333;border-radius:6px;color:var(--text);font-size:0.8rem;margin-right:6px">
          ${zoneOptions}
        </select>
        <button class="btn btn-outline" style="padding:4px 10px;font-size:0.8rem" onclick="reassign(${d.id}, '${d.name}')">Reassign</button>
      </td>
    </tr>`).join('');

  // set current zone as selected
  drivers.forEach(d => {
    const sel = document.getElementById(`zone-select-${d.id}`);
    if (sel) sel.value = d.zone;
  });
}

function renderDriverChart(drivers) {
  const active = drivers.filter(d => d.status === 'Active').length;
  const idle   = drivers.filter(d => d.status === 'Idle').length;
  const offline= drivers.filter(d => d.status === 'Offline').length;
  const ctx = document.getElementById('driver-chart').getContext('2d');
  if (window._driverChart) window._driverChart.destroy();
  window._driverChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Active', 'Idle', 'Offline'],
      datasets: [{data: [active, idle, offline], backgroundColor: ['#4caf50', '#f5a623', '#f44336'], borderWidth: 0}]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {legend: {labels: {color: '#e0e0e0'}, position: 'bottom'}}
    }
  });
}

async function loadDrivers() {
  try {
    const res = await fetch('/api/driver/list');
    const drivers = await res.json();
    allDrivers = drivers;
    renderDriverTable(drivers);
    renderDriverChart(drivers);

    // update stat cards
    document.querySelector('.stat-card .value').textContent = drivers.length;
    const active  = drivers.filter(d => d.status === 'Active').length;
    const idle    = drivers.filter(d => d.status === 'Idle').length;
    const offline = drivers.filter(d => d.status === 'Offline').length;
    const vals = document.querySelectorAll('.stat-card .value');
    if (vals[1]) vals[1].textContent = active;
    if (vals[2]) vals[2].textContent = idle;
    if (vals[3]) vals[3].textContent = offline;
  } catch {
    document.getElementById('driver-table').innerHTML =
      '<tr><td colspan="5" style="color:#f44336">Failed to load drivers.</td></tr>';
  }
}

async function reassign(userId, name) {
  const zone = document.getElementById(`zone-select-${userId}`).value;
  const message = `📍 You have been reassigned to ${zone.charAt(0).toUpperCase()+zone.slice(1)} zone. Please head there immediately.`;
  try {
    const res = await fetch('/api/driver/notify', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_id: userId, message, zone})
    });
    if (res.ok) {
      showToast(`✅ ${name} reassigned to ${zone} and notified.`);
      loadDrivers();
    } else {
      showToast(`❌ Failed to notify ${name}.`, true);
    }
  } catch {
    showToast('❌ Server error.', true);
  }
}

async function applyAllocation() {
  if (!allDrivers.length) { showToast('❌ No drivers loaded.', true); return; }

  // assign each suggestion zone to available drivers round-robin
  const available = allDrivers.filter(d => d.status !== 'Offline');
  if (!available.length) { showToast('❌ No active/idle drivers available.', true); return; }

  const notifications = [];
  suggestions.forEach((s, i) => {
    const driver = available[i % available.length];
    notifications.push({
      user_id: driver.id,
      message: `🎯 Allocation update: Please move to ${s.label} zone. Demand: ${s.recommended} drivers needed. Reason: ${s.reason}`,
      zone: s.zone
    });
  });

  try {
    const res = await fetch('/api/driver/notify-all', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({notifications})
    });
    const data = await res.json();
    showToast(`✅ ${data.message} — All drivers have been notified.`);
    loadDrivers();
  } catch {
    showToast('❌ Failed to apply suggestions.', true);
  }
}

function showToast(msg, isError = false) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.style.cssText = 'position:fixed;bottom:30px;right:30px;padding:14px 20px;border-radius:10px;font-size:0.9rem;z-index:9999;transition:opacity 0.4s';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.background = isError ? '#f44336' : '#4caf50';
  toast.style.color = '#fff';
  toast.style.opacity = '1';
  setTimeout(() => toast.style.opacity = '0', 3000);
}

document.addEventListener('DOMContentLoaded', () => {
  renderSuggestions();
  loadDrivers();
});
