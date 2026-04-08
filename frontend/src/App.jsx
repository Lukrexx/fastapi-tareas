import { useState } from "react"

const API = "https://fastapi-tareas-hymb.onrender.com"

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [token, setToken] = useState("")

  const login = async () => {
    const res = await fetch(`${API}/auth/login?username=${username}&password=${password}`, {
      method: "POST"
    })

    const data = await res.json()
    setToken(data.access_token)
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Login</h1>

      <input
        placeholder="usuario"
        onChange={e => setUsername(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="password"
        type="password"
        onChange={e => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={login}>Login</button>

      <h3>Token:</h3>
      <p>{token}</p>
    </div>
  )
}

export default App