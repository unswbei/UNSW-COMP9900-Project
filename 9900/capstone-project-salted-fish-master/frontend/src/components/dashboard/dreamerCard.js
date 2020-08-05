import React, { useState } from "react";
import M from "materialize-css";
import { Redirect } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import { connect } from "react-redux";

class DreamerCard extends React.Component {
  constructor() {
    super();
  }

  state = {
    info: [],
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
    const url = "/dreamer/" + this.props.match.params.id;
    const res = await axios.get(url, config);

    this.setState({ info: res.data.Dreamer_Info });
    console.log(this.state.info);
  }

  render() {
    const url =
      "https://api.adorable.io/avatars/140/" + Math.floor(Math.random() * 500);
    const dinfoUrl = "/dreamer/" + this.props.id;

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
                        <h4 className="left event-title">DREAMER INFO</h4>
                      </div>
                    </nav>
                    <div className="container1">
                      <div className="cover-photo">
                        <img src={url} className="profile" />
                      </div>

                      <div
                        className="profile-name center-align"
                        style={{
                          marginLeft: "30px",
                          position: "relative",
                          bottom: "6px",
                        }}
                      >
                        {this.state.info.name}
                      </div>
                      <p
                        className="about"
                        style={{ position: "relative", bottom: "6px" }}
                      >
                        This is {this.state.info.name}'s profile as a dreamer
                      </p>
                      <button
                        className="msg-btn button1"
                        style={{ visibility: "hidden" }}
                        onClick={(e) => this.update(e)}
                      >
                        a
                      </button>

                      <div>
                        <div>
                          <i className="fab material-icons icon">call</i>{" "}
                          <span style={{ position: "relative", bottom: "6px" }}>
                            {this.state.info.phone_no}
                          </span>
                        </div>
                        <div>
                          <i className="fab material-icons icon">email</i>{" "}
                          <span style={{ position: "relative", bottom: "6px" }}>
                            {this.state.info.email}
                          </span>
                        </div>

                        <div>
                          <i className="fab material-icons icon">trending_up</i>{" "}
                          <span style={{ position: "relative", bottom: "4px" }}>
                            {this.state.info.user_level}
                          </span>
                        </div>
                      </div>
                    </div>
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
  id: state.auth.id,
});

export default connect(mapStateToProps, null)(DreamerCard);
