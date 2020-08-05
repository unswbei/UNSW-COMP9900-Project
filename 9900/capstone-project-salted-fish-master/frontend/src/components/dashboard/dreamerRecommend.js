import React, { useState } from "react";
import M from "materialize-css";
import { Redirect } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import DreamerOwnRecommend from "./dreamerOwnRecommend";
import { connect } from "react-redux";

class DreamerRecommend extends React.Component {
  constructor() {
    super();
    this.state = {
      drecommend: [],
    };
  }

  async componentDidMount() {
    M.AutoInit();
    const a = localStorage.getItem("token");

    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };

    const res = await axios.get("/dreamer/recommendation", config);
    var b = res.data.collaborators;
    console.log(b);
    this.setState({ drecommend: b });
  }

  render() {
    if (!this.props.isAuthenticated) {
      return <Redirect to="/login" />;
    }
    if (this.props.authRole !== "Dreamer") {
      return <Redirect to="/colladash" />;
    }

    const dinfoUrl = "/dreamer/" + this.props.id
    return (
      <div>
        <header>
          <div className="navbar-fixed" style={{ position: "fixed" }}>
            <Link
              data-target="nav-mobile"
              className="sidenav-trigger"
              style={{ zIndex: 1 }}
            >
              <i className="material-icons">menu</i>
            </Link>
          </div>
          <div>
            <ul
              id="nav-mobile"
              className="sidenav sidenav-fixed"
              style={{ position: "fixed" }}
            >
              <li className="bold">
                <Link className="waves-effect waves-teal" to="/dashboard">
                  My Projects
                </Link>
              </li>
              <li className="bold">
                <Link className="waves-effect waves-teal" to="/drecommend">
                  Recommend Collaborators
                </Link>
              </li>

              <li className="bold">
                <Link className="waves-effect waves-teal" to={dinfoUrl}>
                  My Info
                </Link>
              </li>

            </ul>
          </div>
        </header>

        <main>
          <div className="container">
            <div className="row">
              <div className="col s12 l12 dashboard">
                <div className="card grey lighten-3">
                  <div className="card-content posts">
                    <nav className="pink darken-1">
                      <div className="nav-wrapper">
                        <h4 className="left event-title">RECOMMENDATION</h4>
                      </div>
                    </nav>

                    {this.state.drecommend.length !== 0 ? (
                      this.state.drecommend.map((each, index) => (
                        <DreamerOwnRecommend each={each} key={index} />
                      ))
                    ) : (
                      <p>Currently we have no recommended collaborators for you. Maybe you need to create a project and some roles to receive recommendations.</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>  
        </main>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  authRole: state.auth.role,
  isAuthenticated: state.auth.isAuthenticated,
  id: state.auth.id,
});

export default connect(mapStateToProps, null)(DreamerRecommend);
