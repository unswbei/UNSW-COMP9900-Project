import React, { Component } from "react";
import DreamerRegis from "./DreamerRegis";
import CollaRegis from "./CollaRegis";
import { Link } from "react-router-dom";
import M from "materialize-css";

class Register extends Component {
  state = {
    dreamer: true,
  };

  componentDidMount() {
    // Auto initialize all the materailize css!
    M.AutoInit();
  }

  handleClickDre() {
    this.setState({ dreamer: true });
  }

  handleClickCol() {
    this.setState({ dreamer: false });
  }

  render() {
    return (
      <div>
        <div className="container">
          <div className="valign-wrapper" style={{ marginTop: "50px" }}>
            <div className="row center">
              <div className="col s12 m10 l12 card-panel z-depth-6">
                <h5 className="avatar">Create Your Account</h5>
                <div>
                  Are you a{" "}
                  <button
                    className="btn-small blue-grey lighten-1 lighten-1 z-depth-0 avatar"
                    onClick={this.handleClickDre.bind(this)}
                  >
                    dreamer
                  </button>
                  <span> or </span>
                  <button
                    className="btn-small blue-grey lighten-1 lighten-1 z-depth-0 avatar"
                    onClick={this.handleClickCol.bind(this)}
                  >
                    collaborator
                  </button>
                </div>
                {this.state.dreamer ? <DreamerRegis /> : <CollaRegis />}
                <div>
                  Already have an account? <Link to="./login">Sign In</Link>
                  <br/>
                  <br/>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Register;
