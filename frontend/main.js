const API = 'http://127.0.0.1:8000';
let token = '';

const qs = (s) => document.querySelector(s);
const setMsg = (id, msg) => (qs(id).textContent = msg);

qs('#loginBtn').onclick = async () => {
  const username = qs('#username').value.trim();
  const password = qs('#password').value.trim();
  const res = await fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) { setMsg('#authMsg', 'Login failed'); return; }
  const data = await res.json();
  token = data.access_token;
  setMsg('#authMsg', 'Logged in');
  loadHistory();
};

qs('#predictBtn').onclick = async () => {
  const payload = {
    age: Number(qs('#age').value),
    gender: Number(qs('#gender').value),
    height: Number(qs('#height').value),
    weight: Number(qs('#weight').value),
    duration: Number(qs('#duration').value),
    heart_rate: Number(qs('#heart_rate').value),
    body_temp: Number(qs('#body_temp').value)
  };
  const res = await fetch(`${API}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload)
  });
  if (!res.ok) { qs('#predOut').textContent = 'Predict failed'; return; }
  const data = await res.json();
  qs('#predOut').textContent = `Calories: ${data.calories.toFixed(0)}`;
  loadHistory();
};

async function loadHistory() {
  const res = await fetch(`${API}/history`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) return;
  const rows = await res.json();
  const tbody = qs('#histTable tbody');
  tbody.innerHTML = rows.map(r => `
    <tr>
      <td>${r.created_at}</td>
      <td>${r.calories.toFixed(0)}</td>
      <td>${r.age}</td>
      <td>${r.gender}</td>
      <td>${r.height}</td>
      <td>${r.weight}</td>
      <td>${r.duration}</td>
      <td>${r.heart_rate}</td>
      <td>${r.body_temp}</td>
    </tr>
  `).join('');
}


