import React, { useState } from "react";
import M from "materialize-css";
import { Redirect } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import CollaOwnProject from "./collaOwnProject";
import { connect } from "react-redux";

class CollaOwnRecommend extends React.Component {
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

    const res = await axios.get("/collaborator/recommendation", config);
    console.log("colla project", res.data);
    this.setState({ myProjects: res.data.projects });
  }

  render() {
    const category_list = [
      "All other",
      "A web based application",
      "A desktop application",
      "A mobile application",

      "A library for other project to reference",

      "A modification to existing platform",
      "A research oriented project",
    ];
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
                        <h4 className="left event-title">RECOM</h4>
                      </div>
                    </nav>
                    {this.state.myProjects.length > 0 ? (
                      this.state.myProjects.map((each, index) => {
                        return (
                          <CollaOwnProject
                            key={index}
                            title={each.title}
                            description={each.description}
                            category={category_list[each.category]}
                            id={each.id}
                            create_time={each.create_time}
                            last_update={each.last_update}
                          />
                        );
                      })
                    ) : (
                      <p>Apply for your first project</p>
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
});

export default connect(mapStateToProps, null)(CollaOwnRecommend);
