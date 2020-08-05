import React, { useState } from "react";
import M from "materialize-css";
import { Redirect } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import { connect } from "react-redux";

class CollaApply extends React.Component {
  constructor() {
    super();
  }

  state = {
    myProjects: [],
  };

  async componentDidMount() {
    // Auto initialize all the materailize css!
    M.AutoInit();
    const a = localStorage.getItem("token");

    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };

    const res = await axios.get("/collaborator/my_applications", config);
    console.log("colla project", res.data);
    this.setState({ myProjects: res.data.applications });
  }

  render() {
    if (!this.props.isAuthenticated) {
      return <Redirect to="/login" />;
    }
    if (this.props.authRole !== "Collaborator") {
      return <Redirect to="/dashboard" />;
    }
    return (
      <div>
        <header>
          <div className="navbar-fixed" style={{ position: "fixed" }}>
            <Link data-target="nav-mobile" className="sidenav-trigger">
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
                <Link className="waves-effect waves-teal" to="./colladash">
                  My Projects
                </Link>
              </li>
              <li className="bold">
                <Link className="waves-effect waves-teal" to="./crecommend">
                  Recommend Projects
                </Link>
              </li>

              <li className="bold">
                <Link className="waves-effect waves-teal" to="./apply">
                  Apply Projects
                </Link>
              </li>

              <li className="bold">
                <Link className="waves-effect waves-teal" to="./invited">
                  Invited Projects
                </Link>
              </li>

              <li className="bold">
                <Link className="waves-effect waves-teal" to="./cinfo">
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
                        <h4 className="left event-title">Apply projects</h4>
                      </div>
                    </nav>
                    <div className="right">
                      Total:{" "}
                      {this.state.myProjects && this.state.myProjects.length}{" "}
                      apply times
                    </div>
                    <br></br>
                    {this.state.myProjects &&
                      this.state.myProjects.map((each, index) => {
                        const url = "/projects/" + each.projectID;
                        const url1 = "/dreamer/" + each.Invitor;
                        return (
                          <div key={index}>
                            <br></br>
                            <div>
                              <Link to={url}>Project {each.project_title}</Link>
                              : You have applied the role "{each.Role_title}"
                              and leave the messages "{each.General_text}"
                              <span className="right">
                                status: {each.Application_status}
                              </span>
                            </div>
                          </div>
                        );
                      })}
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
});

export default connect(mapStateToProps, null)(CollaApply);
