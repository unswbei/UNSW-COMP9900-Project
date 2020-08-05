import React, { useState } from "react";
import { connect } from "react-redux";
import { setAlert } from "../../actions/alert";
import { loginUser } from "../../actions/auth";
import { Redirect } from "react-router-dom";
import M from "materialize-css";
import Dashboard from "../dashboard/Dashboard";

const LoginForm = (props) => {
  function componentDidMount() {
    // Auto initialize all the materailize css!
    M.AutoInit();
  }
  componentDidMount();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const { role, loginUser, isAuthenticated,authRole } = props;
  const { email, password } = formData;

  const onChange = (e) => {
    // get target element name
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onSubmit = (e) => {
    e.preventDefault();
    loginUser(email, password, role);
    console.log("success");
  };

  if (authRole==="Dreamer" && isAuthenticated) {
    return <Redirect to="/dashboard" />;
  }else if(authRole==="Collaborator" && isAuthenticated){
    return <Redirect to="/colladash" />;
  }else if(authRole==="Admin" && isAuthenticated){
    return <Redirect to="/admindash"/>
  }

  return (
    <form onSubmit={(e) => onSubmit(e)}>
      <div className="input-field">
        <input
          type="email"
          // placeholder="Email Address"
          name="email"
          value={email}
          onChange={(e) => onChange(e)}
          required
          id="email_address"
        />
        <label for="email_address">Email Address</label>
      </div>
      <div className="input-field">
        <input
          type="password"
          // placeholder="Password"
          name="password"
          minLength="8"
          value={password}
          onChange={(e) => onChange(e)}
          required
          id="password"
        />
        <label for="password">Password</label>
      </div>
      <p className="yellow">You will log in as {role}</p>
      <input type="submit" className="btn btn-primary blue-grey darken-1" value="Sign in" />
    </form>
  );
};

const mapStateToProps = (state) => ({
  isAuthenticated: state.auth.isAuthenticated,
  authRole: state.auth.role,
});

export default connect(mapStateToProps, { loginUser })(LoginForm);
