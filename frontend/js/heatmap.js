// heatmap.js — Demand heatmap renderer

const zones = ['Downtown', 'Airport', 'Suburbs', 'Mall', 'Hospital', 'University', 'Station', 'Business Park'];
const hours = ['12AM','2AM','4AM','6AM','8AM','10AM','12PM','2PM','4PM','6PM','8PM','10PM'];
const hourValues = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22];

function getDemand(zone, hourIndex) {
  const base = [87, 72, 34, 65, 48, 55, 91, 43];
  const hourMultiplier = [0.05, 0.03, 0.02, 0.15, 0.9, 0.6, 0.55, 0.5, 0.65, 1.0, 0.85, 0.6];
  return Math.round(base[zone] * hourMultiplier[hourIndex]);
}

function getColor(value) {
  if (value < 10) return '#1a3a1a';
  if (value < 25) return '#2d6a2d';
  if (value < 45) return '#f5a623';
  if (value < 65) return '#e05c00';
  return '#c0392b';
}

function renderHeatmap() {
  const container = document.getElementById('heatmap-container');
  container.innerHTML = '';

  const selectedHour = document.getElementById('heatmap-hour').value;

  // Filter hours based on selection
  let displayHours, displayIndices;
  if (selectedHour === '') {
    displayHours = hours;
    displayIndices = hours.map((_, i) => i);
  } else {
    const hi = hourValues.findIndex(h => h === parseInt(selectedHour));
    const idx = hi >= 0 ? hi : 0;
    displayHours = [hours[idx]];
    displayIndices = [idx];
  }

  // Update grid columns
  container.style.gridTemplateColumns = `80px repeat(${displayHours.length}, minmax(40px, 80px))`;

  // Header row
  container.appendChild(Object.assign(document.createElement('div'), {
    style: 'font-size:0.65rem;color:var(--muted);display:flex;align-items:center',
    textContent: 'Zone'
  }));
  displayHours.forEach(h => {
    const el = document.createElement('div');
    el.style.cssText = 'font-size:0.6rem;color:var(--muted);text-align:center;padding:2px';
    el.textContent = h;
    container.appendChild(el);
  });

  // Data rows
  zones.forEach((zone, zi) => {
    const label = document.createElement('div');
    label.style.cssText = 'font-size:0.65rem;color:var(--muted);display:flex;align-items:center;padding-right:4px';
    label.textContent = zone;
    container.appendChild(label);

    displayIndices.forEach(hi => {
      const val = getDemand(zi, hi);
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      cell.style.background = getColor(val);
      cell.style.minHeight = '22px';
      cell.style.fontSize = '0.55rem';
      cell.title = `${zone} at ${hours[hi]}: ${val} rides`;
      cell.textContent = val > 5 ? val : '';
      container.appendChild(cell);
    });
  });

  // Hotspot list
  const hotspots = zones.map((z, i) => ({
    name: z,
    peak: Math.max(...displayIndices.map(hi => getDemand(i, hi)))
  })).sort((a, b) => b.peak - a.peak).slice(0, 4);

  document.getElementById('hotspot-list').innerHTML = hotspots.map(h => `
    <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #2a2a4a">
      <span>${h.name}</span>
      <div>
        <span style="color:var(--danger);font-weight:700">${h.peak}</span>
        <span style="color:var(--muted);font-size:0.8rem"> rides/hr peak</span>
      </div>
    </div>`).join('');
}

document.addEventListener('DOMContentLoaded', renderHeatmap);
