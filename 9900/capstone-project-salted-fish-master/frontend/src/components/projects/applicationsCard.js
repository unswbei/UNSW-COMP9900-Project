import React from "react";
import M from "materialize-css";
import { Link } from "react-router-dom";
import axios from "axios";
import { Modal, Button } from "react-materialize";
import { sendInvitation, approve, decline } from "../../actions/projects";
import { connect } from "react-redux";

class ApplicationCard extends React.Component {
  constructor() {
    super();
    this.state = {
      info: {},
      general_text: "",
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
    console.log(this.props.match.params.aid);
    const res = await axios.get(
      "/collaborator/" + this.props.match.params.aid,
      config
    );
    console.log(res.data);
    this.setState({ info: res.data });
  }

  handleonChange = (e) => {
    // get target element name
    this.setState({ [e.target.name]: e.target.value });
  };

  handleonSubmit = (e) => {
    e.preventDefault();

    const { general_text } = this.state;
    const pid = this.props.match.params.pid;
    const rid = this.props.match.params.rid;
    const cid = this.props.match.params.cid;
    this.props.sendInvitation({ general_text, pid, rid, cid });
  };

  approveApplication(e) {
    const pid = this.props.match.params.pid;
    const rid = this.props.match.params.rid;
    const aid = this.props.match.params.cid;
    this.props.approve({ aid, rid, pid });
  }

  async declineApplication(e) {
    const pid = this.props.match.params.pid;
    const rid = this.props.match.params.rid;
    const aid = this.props.match.params.cid;
    await this.props.decline({ aid, rid, pid });
  }

  render() {
    const url =
      "https://api.adorable.io/avatars/140/" + Math.floor(Math.random() * 500);

    const a = { 0: "entry", 1: "medium", 2: "senior", 3: "professional" };

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
                        <h4 className="left event-title">
                          COLLARBORATOR INFOMATION
                        </h4>
                        <form className="search-field right">
                          <div className="input-field">
                            <input id="search" type="search" required />
                            <label
                              className="label-icon search-icon"
                              for="search"
                            >
                              <i className="material-icons">search</i>
                            </label>
                            <i className="material-icons close-icon">close</i>
                          </div>
                        </form>
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
                      <button
                        className="msg-btn button1"
                        onClick={(e) => this.approveApplication(e)}
                      >
                        Approve
                      </button>

                      <Button
                        waves="follow-btn button1"
                        style={{ marginLeft: "10px" }}
                        onClick={(e) => this.declineApplication(e)}
                      >
                        Decline
                      </Button>

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
                                      <span>
                                        {skill_list[key]}:{" "}
                                        {this.state.info.Skills[key]} years{" "}
                                      </span>
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
});

export default connect(mapStateToProps, { sendInvitation, approve, decline })(
  ApplicationCard
);
