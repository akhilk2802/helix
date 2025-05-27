import { useState } from 'react';
import "../styles/scss/Signup.scss";
import { Container, Form, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom'

interface SignupProps { onSwitchToLogin: () => void }
const Signup: React.FC<SignupProps> = ({ onSwitchToLogin }) => {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("")
  const [company, setCompany] = useState("")

  const handleSubmit = async (e:React.FormEvent) => {
    e.preventDefault();

    const apiUrl = process.env.REACT_APP_API_URL;
    const port = process.env.REACT_APP_PORT;

    try{
      const response = await fetch(`${apiUrl}:${port}/api/user/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password, company, name })
      });

      const data = await response.json();
      console.log("data -> ", data)

      if (response.ok) {
        // console.log("Signup successful", data);
        localStorage.setItem("user", JSON.stringify(data.user));
        setEmail("")
        setPassword("")
        setName("")
        setCompany("")
        navigate("/");
        alert("Signup Successful! proceed to login")
      } else {
        alert(data.error || "Signup failed");
      }


    } catch(err) {
      console.error("Signup error:", err);
      alert("Something went wrong. Please try again.");
    }
  };

  
  return (
      <Container className="signup-container">
        <div className="signup-card">
          <div className="signup-header">
            <span className="helix-logo">🧬</span>
            <span className="helix-brand">Helix</span>
          </div>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label className="visually-hidden">Name</Form.Label>
              <Form.Control type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)}/>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label className="visually-hidden">Email address</Form.Label>
              <Form.Control type="email" placeholder="Email Address" value={email} onChange={(e) => setEmail(e.target.value)}/>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label className="visually-hidden">Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label className="visually-hidden">Company</Form.Label>
              <Form.Control type="text" placeholder="Where do you work ?" value={company} onChange={(e) => setCompany(e.target.value)}/>
            </Form.Group>
            <Button className="signup-btn" type="submit">
              Sign Up
            </Button>
            <div className="signup-switch">
              <span>Already have an account? </span>
              <a
                href="#"
                className="fw-bold"
                onClick={e => { e.preventDefault(); onSwitchToLogin(); }}
              >
                Login!
              </a>
            </div>
          </Form>
        </div>
      </Container>
);
};

export default Signup;