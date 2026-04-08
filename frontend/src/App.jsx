import { useState } from "react"

const API = "https://fastapi-tareas-hymb.onrender.com"

console.log("CLICK LOGIN")

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [token, setToken] = useState("")

  const login = async () => {
  const res = await fetch(`${API}/auth/login?username=${username}&password=${password}`, {
    method: "POST"
  })

  const data = await res.json()

  console.log("STATUS:", res.status)
  console.log("DATA:", data)
  localStorage.setItem("token", data.access_token)
  setToken(JSON.stringify(data, null, 2))
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

    <h3>Token:</h3>
    <p>{token}</p>
  </div>
)
}

export default App