import React, {useEffect, useState} from "react";
import {createRoot} from "react-dom/client";
import {A2UIRenderer} from "./Renderer.jsx";
import "@agent-nebula/a2ui-rich/styles.css";
import "./styles.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/a2ui")
      .then((response) => {
        if (!response.ok) throw new Error(`A2UI request failed: ${response.status}`);
        return response.json();
      })
      .then((payload) => setMessages(payload.messages ?? []))
      .catch((reason) => setError(reason.message));
  }, []);

  async function handleAction(action, dataModel) {
    setError(null);
    try {
      const response = await fetch("/api/a2ui/action", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({action, dataModel}),
      });
      if (!response.ok) throw new Error(`A2UI action failed: ${response.status}`);
      const payload = await response.json();
      setMessages(payload.messages ?? []);
    } catch (reason) {
      setError(reason.message);
    }
  }

  return <main className="example-shell">
    <header><p className="eyebrow">Agent Nebula SecureAgent Example</p><h1>A2UI v1.0 Browser Validation</h1></header>
    {error ? <div role="alert" className="error">{error}</div> : null}
    {!error && messages.length === 0 ? <p>Loading A2UI surface…</p> : null}
    <A2UIRenderer ui={messages} onAction={handleAction}/>
  </main>;
}

createRoot(document.getElementById("root")).render(<App/>);
