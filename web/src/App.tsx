import './App.css'
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import ReactECharts from 'echarts-for-react'
import { useState } from 'react'

const API = 'http://127.0.0.1:8000'

function Login({ onToken }: { onToken: (t: string) => void }) {
  const navigate = useNavigate()
  const [username, setUsername] = useState('demo')
  const [password, setPassword] = useState('demo123!')
  const [msg, setMsg] = useState('')

  const login = async () => {
    if (!username || !password) { setMsg('Enter username and password'); return }
    const res = await fetch(`${API}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }) })
    if (!res.ok) { setMsg('Login failed'); return }
    const data = await res.json()
    onToken(data.access_token)
    navigate('/')
  }

  return (
    <div className="card">
      <h2>Login</h2>
      <input placeholder="username" value={username} onChange={e => setUsername(e.target.value)} />
      <input placeholder="password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={login}>Login</button>
      <div>{msg}</div>
    </div>
  )
}

function Dashboard({ token }: { token: string }) {
  const [form, setForm] = useState({ age: 25, gender: 0, height: 175, weight: 70, duration: 45, heart_rate: 140, body_temp: 37.5 })
  const [cal, setCal] = useState<number | null>(null)
  const [rows, setRows] = useState<any[]>([])

  const predict = async () => {
    for (const [k, v] of Object.entries(form)) {
      if (v === null || v === undefined || (typeof v === 'number' && isNaN(v))) return
    }
    const res = await fetch(`${API}/predict`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify(form) })
    if (!res.ok) return
    const data = await res.json(); setCal(data.calories)
    loadHistory()
  }

  const loadHistory = async () => {
    const res = await fetch(`${API}/history`, { headers: { Authorization: `Bearer ${token}` } })
    if (!res.ok) return
    setRows(await res.json())
  }

  const chartOptions = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    grid: { left: 40, right: 20, top: 30, bottom: 40 },
    xAxis: { type: 'category', data: rows.map(r => r.created_at), axisLabel: { color: '#94a3b8' } },
    yAxis: { type: 'value', name: 'Calories', axisLabel: { color: '#94a3b8' }, splitLine: { lineStyle: { color: '#1f2937' } } },
    series: [{
      name: 'Calories',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      itemStyle: { color: '#60a5fa' },
      areaStyle: { color: 'rgba(96,165,250,0.15)' },
      data: rows.map(r => Math.round(r.calories))
    }]
  }

  return (
    <div className="card">
      <h1 className="title">Dashboard</h1>

      <section className="about">
        <p>
          This system provides real-time fitness and health tracking with intelligent movement analysis, routine logging,
          goal tracking, and progress visualization in a single, user-friendly interface. Users can monitor workout reps,
          calorie burn, hydration, and more — with instant visual feedback, weekly summaries, and progress charts.
          All processing is local to maintain privacy and low system overhead. By integrating smart tracking, health
          analytics, and real-time interaction, it promotes a consistent, safe, and engaging fitness journey.
        </p>
        <p className="muted">
          The model predicts total calories burned (regression) from personal metrics (age, gender, height, weight)
          and exercise metrics (duration, heart rate, body temperature).
        </p>
      </section>

      <div className="grid labeled">
        <label>
          <span>Age</span>
          <input placeholder="Age" value={form.age} onChange={e => setForm({ ...form, age: Number(e.target.value) })} />
        </label>
        <label>
          <span>Gender (0 male, 1 female)</span>
          <input placeholder="Gender" value={form.gender} onChange={e => setForm({ ...form, gender: Number(e.target.value) })} />
        </label>
        <label>
          <span>Height (cm)</span>
          <input placeholder="Height" value={form.height} onChange={e => setForm({ ...form, height: Number(e.target.value) })} />
        </label>
        <label>
          <span>Weight (kg)</span>
          <input placeholder="Weight" value={form.weight} onChange={e => setForm({ ...form, weight: Number(e.target.value) })} />
        </label>
        <label>
          <span>Duration (min)</span>
          <input placeholder="Duration" value={form.duration} onChange={e => setForm({ ...form, duration: Number(e.target.value) })} />
        </label>
        <label>
          <span>Heart Rate (bpm)</span>
          <input placeholder="Heart Rate" value={form.heart_rate} onChange={e => setForm({ ...form, heart_rate: Number(e.target.value) })} />
        </label>
        <label>
          <span>Body Temp (°C)</span>
          <input placeholder="Body Temp" value={form.body_temp} onChange={e => setForm({ ...form, body_temp: Number(e.target.value) })} />
        </label>
      </div>

      <div className="actions">
        <button onClick={predict}>Predict</button>
        <div className="calories">Calories: {cal?.toFixed?.(0) ?? '-'}</div>
        <button onClick={loadHistory}>Load History</button>
      </div>

      <ReactECharts option={chartOptions} notMerge style={{ height: '300px', width: '100%' }} />

      <table>
        <thead><tr><th>when</th><th>cal</th><th>age</th><th>hr</th></tr></thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.id}><td>{r.created_at}</td><td>{r.calories.toFixed(0)}</td><td>{r.age}</td><td>{r.heart_rate}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function App() {
  const [token, setToken] = useState<string | null>(null)
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login onToken={setToken} />} />
        <Route path="/" element={token ? <Dashboard token={token} /> : <Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  )
}
