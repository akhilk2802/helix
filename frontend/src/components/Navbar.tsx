import React from 'react';
import "../styles/scss/Navbar.scss"
import DnaSvg from "twemoji/assets/svg/1f9ec.svg"

const Navbar: React.FC = () => (
  <nav className="navbar">
    <div className="container">
        <a className="navbar-brand" href="#">
        {/* <img src={DnaSvg} alt="DNA" width="30" height="24"/> */}
        Helix AI
        </a>
    </div>
    </nav>
);

export default Navbar;