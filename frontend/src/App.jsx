import { useState } from "react"

const API = "http://127.0.0.1:8000"

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [token, setToken] = useState("")

  const login = async () => {
    console.log("CLICK LOGIN")

    const res = await fetch(`${API}/auth/login?username=${username}&password=${password}`, {
      method: "POST"
    })

    const data = await res.json()

    console.log("STATUS:", res.status)
    console.log("DATA:", data)

    setToken(data.access_token)
    localStorage.setItem("token", data.access_token)
  }
  const [tareas, setTareas] = useState([])
  const obtenerTareas = async () => {
  const token = localStorage.getItem("token")

  const res = await fetch(`${API}/tareas/tareas`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  const data = await res.json()

  console.log("TAREAS:", data)

  setTareas(data)
}

  return (
    <div style={{ padding: 20 }}>
      <h1>Login</h1>

      <input
        placeholder="usuario"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <br /><br />

      <input
        type="password"
        placeholder="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={login}>Login</button>
      <button onClick={obtenerTareas}>Ver tareas</button>

      <ul>
        {tareas.map((t) => (
          <li key={t.id}>{t.nombre}</li>
        ))}
      </ul>

      <h3>Token:</h3>
      <p>{token}</p>
    </div>
  )
}

export default App