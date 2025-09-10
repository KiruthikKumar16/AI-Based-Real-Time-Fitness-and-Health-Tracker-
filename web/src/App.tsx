import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState } from 'react'

const API = 'http://127.0.0.1:8000'

function Login({ onToken }: { onToken: (t: string) => void }) {
  const [username, setUsername] = useState('demo')
  const [password, setPassword] = useState('demo123!')
  const [msg, setMsg] = useState('')

  const login = async () => {
    if (!username || !password) { setMsg('Enter username and password'); return }
    const res = await fetch(`${API}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }) })
    if (!res.ok) { setMsg('Login failed'); return }
    const data = await res.json()
    onToken(data.access_token)
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

  return (
    <div className="card">
      <h2>Dashboard</h2>
      <div className="grid">
        {(['age','gender','height','weight','duration','heart_rate','body_temp'] as const).map(k => (
          <input key={k} placeholder={k} value={(form as any)[k]} onChange={e => setForm({ ...form, [k]: Number(e.target.value) })} />
        ))}
      </div>
      <button onClick={predict}>Predict</button>
      <div>Calories: {cal?.toFixed?.(0) ?? '-'}</div>
      <button onClick={loadHistory}>Load History</button>
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
