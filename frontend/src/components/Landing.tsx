import React, {useState} from "react";
import "../styles/scss/Landing.scss"
import Navbar from "./Navbar"
import Login from "./Login"
import Signup from "./Signup"
import Header from "./Header"
import Home from "./Home"
import {Row, Col, Container } from 'react-bootstrap'
import helixagent from "../assets/helixagent.png"

const Landing: React.FC = () => {
  const [isSignup, setIsSignup] = useState(false);

  return (
  <Container fluid className="homepage">
    <Container fluid className="hero">
      <Container  className="login">
        <Row>
          <Col>
          <div className="landing-image">
            <img src={helixagent}></img>
          </div>
          </Col>
          <Col>
            { isSignup ? (
              <Signup onSwitchToLogin={() => setIsSignup(false)} />
            ):(
            <Login onSwitchToSignup={() => setIsSignup(true)}/>
            )}
          </Col>
        </Row>
      </Container>
    </Container>
  </Container>
);};

export default Landing;