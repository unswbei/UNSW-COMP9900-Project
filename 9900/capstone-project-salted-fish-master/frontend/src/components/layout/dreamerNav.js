import React from "react";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { logOut } from "../../actions/auth";
import { Redirect } from "react-router-dom";

const DreamerNav = ({ isAuthenticated, logOut }) => {
  if (!isAuthenticated) return <Redirect to="/login" />;

  return (
    <nav className="darken-2 nav-wrapper blue-grey lighten-1 navbar-css">
      <Link to="/" className="brand-logo avatar">
        FindColla
      </Link>

      <ul className="right hide-on-med-and-down">
        <li>
          <Link to="/projects" className="avatar">
            Projects
          </Link>
        </li>
        <li>
          <Link to="/create" className="avatar">
            Create Project
          </Link>
        </li>
        <li>
          <Link to="/dashboard" className="avatar">
            dashboard
          </Link>
        </li>
        <li>
          <Link to="/login" onClick={logOut} className="avatar">
            Sign out
          </Link>
        </li>
      </ul>
    </nav>
  );
};
const mapStateToProps = (state) => ({
  isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { logOut })(DreamerNav);
