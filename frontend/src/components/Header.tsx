import "../styles/scss/Header.scss";
import { Dropdown } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const Header: React.FC = () => {
  
  const navigate = useNavigate();

  const handleSignOut = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("user_sessionId")
    navigate("/");
  };

  return (
    <header className="helix-app-header">
      <div className="header-left">
        <span className="helix-logo">🧬</span>
        <span className="helix-brand">Helix</span>
      </div>
      <div className="header-right">
        <Dropdown align="end">
          <Dropdown.Toggle variant="light" className="profile-toggle">
            <span className="profile-avatar">A</span>
          </Dropdown.Toggle>
          <Dropdown.Menu>
            <Dropdown.Item onClick={handleSignOut}>Sign out</Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </div>
    </header>
  );
};

export default Header;