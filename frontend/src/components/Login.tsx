import { useState } from 'react';
import { Container, Form, Button } from "react-bootstrap";
import "../styles/scss/Login.scss";
import { useNavigate } from 'react-router-dom'
import { v4 as uuidv4 } from "uuid";


interface LoginProps { onSwitchToSignup: () => void }
const Login: React.FC<LoginProps> = ({ onSwitchToSignup }) => {

  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const apiUrl = process.env.REACT_APP_API_URL;
    const port = process.env.REACT_APP_PORT;

    try {
      const response = await fetch(`${apiUrl}:${port}/api/user/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      // console.log("data -> ", data)

      if (response.ok) {
        // console.log("Login successful", data);
        localStorage.setItem("user", JSON.stringify(data.user));

        const user_sessionId = Math.random().toString(36).substring(2, 6);
        // console.log("sessaionId from login -> ", sessionId)
        localStorage.setItem("user_sessionId", user_sessionId);

        setEmail("")
        setPassword("")
        navigate("/home");
      } else {
        alert(data.error || "Login failed");
      }

    } catch (err) {
      console.error("Login error:", err);
      alert("Something went wrong. Please try again.");
    }
  };

  return (
  <Container className="login-container">
    <div className="login-card">
      <div className="login-header">
        <span className="helix-logo">🧬</span>
        <span className="helix-brand">Helix</span>
      </div>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label className="visually-hidden">Email address</Form.Label>
          <Form.Control type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label className="visually-hidden">Password</Form.Label>
          <Form.Control type="password" placeholder="Password"  value={password} onChange={(e) => setPassword(e.target.value)}/>
        </Form.Group>
        <Button className="login-btn" type="submit">
          Login
        </Button>
        <div className="login-switch">
          <span>Don't have an account? </span>
          <a
            href="#"
            className="fw-bold"
            onClick={e => { e.preventDefault(); onSwitchToSignup(); }}
          >
            Sign up!
          </a>
        </div>
      </Form>
    </div>
  </Container>
  );
};

export default Login;