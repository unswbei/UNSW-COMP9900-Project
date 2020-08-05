import React, { useState } from "react";
import M from "materialize-css";
import { Redirect } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import { connect } from "react-redux";
import { uploadResume } from "../../actions/projects";

class CollaInfo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedFile: null,
      info: [],
    };
    this.onChangeHandler = this.onChangeHandler.bind(this);
  }

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
    const url = "/collaborator/" + this.props.id;
    const res = await axios.get(url, config);
    this.setState({ info: res.data });
  }

  async update(e) {
    console.log(1);
  }

  async onChangeHandler(event) {
    await this.setState({
      selectedFile: event.target.files[0],
    });
    this.props.uploadResume(this.state.selectedFile);
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
    const a = { 0: "entry", 1: "medium", 2: "senior", 3: "professional", 4:"expert" };
    const url =
      "https://api.adorable.io/avatars/140/" + Math.floor(Math.random() * 500);
    const skill_list = [
      "Web Development",
      "Java",
      "Python",
      "PHP",
      "Script Language",
      "Database Management",
      "Computer Vision",
      "Security Engineering",
      "Testing",
      "Algorithm Design",
      "Operating System",
      "Data Science",
      "Human Computer Interaction",
      "Deep Learning/Neural Network",
      "Distribution System",
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
                        <h4 className="left event-title">EVENTS</h4>
                      </div>
                    </nav>
                    <div className="container1">
                      <div className="cover-photo">
                        <img src={url} className="profile" />
                      </div>
                      <div className="profile-name">{this.state.info.Name}</div>
                      <p className="about">
                        This is {this.state.info.Name}'s profile as a
                        collaborator {this.state.info.Description}
                      </p>
                      <Link to="/collapatch">
                      <button
                        className="msg-btn button1"
                        onClick={(e) => this.update(e)}
                      >
                        update
                      </button>
                      </Link>
                      <button
                        className="msg-btn button1 file-field input-field"
                        style={{ marginLeft: "15px" }}
                      >
                        <span>upload</span>
                        <input
                          type="file"
                          name="file"
                          onChange={(e) => this.onChangeHandler(e)}
                        />
                      </button>
                      <div>
                        <div>
                          <i className="fab material-icons icon">call</i>{" "}
                          <span style={{ position: "relative", bottom: "6px" }}>
                            {this.state.info.Phone_no}
                          </span>
                        </div>
                        <div>
                          <i className="fab material-icons icon">email</i>{" "}
                          <span style={{ position: "relative", bottom: "6px" }}>
                            {this.state.info.Email}
                          </span>
                        </div>
                        <div>
                          <i className="fab material-icons icon">
                            perm_identity
                          </i>{" "}
                          <span style={{ position: "relative", bottom: "6px" }}>
                            {this.state.info.Education}
                          </span>
                        </div>
                        <div>
                          <i className="fab material-icons icon">trending_up</i>{" "}
                          <span style={{ position: "relative", bottom: "4px" }}>
                            {a[this.state.info.User_level]}
                          </span>
                        </div>
                        <div>
                          <span style={{ position: "relative", bottom: "4px" }}>
                            {this.state.info.Skills &&
                              Object.keys(this.state.info.Skills).map((key) => {
                                return (
                                  <div>
                                    {skill_list[key]}:{" "}
                                    {this.state.info.Skills[key]} years{" "}
                                  </div>
                                );
                              })}
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
  authRole: state.auth.role,
  isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { uploadResume })(CollaInfo);
