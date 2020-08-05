import React from "react";
import { Link } from "react-router-dom";

const BeforeAuthNarvbar = () => {
  return (
    <nav className="darken-2 nav-wrapper blue-grey lighten-1 navbar-css">
      <Link to="/" className="brand-logo avatar">
        FindColla
      </Link>
      {/*<a href="#" className="sidenav-trigger right" data-target="mobile-links">*/}
      {/*  <i className="material-icons">*/}
      {/*    menu*/}
      {/*  </i>*/}
      {/*</a>*/}
      <ul className="right hide-on-med-and-down">
        <li>
          <Link to="/projects" className="avatar">
            Projects
          </Link>
        </li>
        <li>
          <Link to="/register" className="avatar">
            Register
          </Link>
        </li>
        <li>
          <Link to="/login" className="avatar">
            Login
          </Link>
        </li>
      </ul>
    </nav>

  );
};

export default BeforeAuthNarvbar;
