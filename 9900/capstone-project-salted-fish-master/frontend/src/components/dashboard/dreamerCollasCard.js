import React from "react";
import M from "materialize-css";
import { Link } from "react-router-dom";
import axios from "axios";
import { Modal, Button } from "react-materialize";
import { sendInvitation, approve } from "../../actions/projects";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

class DreamerCollasCard extends React.Component {
  constructor() {
    super();
    this.state = {
      info: {},
      general_text: "",
      resume: "",
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
    console.log(this.props.match.params.cid);
    const res = await axios.get(
      "/collaborator/" + this.props.match.params.cid,
      config
    );
    console.log(res.data);
    this.setState({ info: res.data });
    const resumeName = await axios.get(
      "/collaborator/" + this.props.match.params.cid + "/resume",
      config
    );
    this.setState({ resume: resumeName.data });
    console.log(this.state.resume);
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

  async approveApplication(e) {
    const pid = this.props.match.params.pid;
    const rid = this.props.match.params.rid;
    const aid = this.props.match.params.cid;
    await this.props.approve({ aid, rid, pid });
  }

  render() {
    const url =
        "https://api.adorable.io/avatars/48/" +
        this.props.id+
        "@adorable.io.png";


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
    if (!this.props.isAuthenticated) {
      return <Redirect to="/login" />;
    }
    const downloadUrl =
        "http://localhost:5000/download/" + this.state.resume.filename;
    // const downloadUrl = "http://gcp.x-zhou.com:5000/download/" + this.state.resume.filename;
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
                <Link className="waves-effect waves-teal" to="/dinfo">
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
                      {/*<button*/}
                      {/*  className="msg-btn button1"*/}
                      {/*  onClick={(e) => this.approveApplication(e)}*/}
                      {/*>*/}
                      {/*  Message*/}
                      {/*</button>*/}

                      <Modal
                        dialogClassName="custom-dialog"
                        trigger={
                          <Button
                            waves="follow-btn button1"
                            style={{ marginLeft: "10px" ,
                                      marginBottom: "10px",
                                      marginTop: "10px"}}
                          >
                            Invite
                          </Button>
                        }
                      >
                        <form
                          className="col s12"
                          onSubmit={(e) => this.handleonSubmit(e)}
                        >
                          <div className="input-field">
                            <label htmlFor="invitation message">
                              Type in the invitation message
                            </label>
                            <input
                              type="text"
                              name="general_text"
                              onChange={(e) => this.handleonChange(e)}
                              required
                              id = "invitation message"
                            />

                          </div>
                          <input
                            type="submit"
                            className="btn-small left"
                            value="send"
                            style={{ marginTop: "38px" }}
                          />
                        </form>
                      </Modal>

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
                          <i className="fab material-icons icon">grade</i>{" "}
                          <span style={{ position: "relative", bottom: "4px" }}>
                            {this.state.info.Skills &&
                              Object.keys(this.state.info.Skills).map((key) => {
                                return (
                                  <div>
                                    {skill_list[key]}:{" "}
                                    {this.state.info.Skills[key]} years
                                  </div>
                                );
                              })}
                          </span>
                        </div>
                        <div>
                          <i className="fab material-icons icon">
                            insert_drive_file
                          </i>{" "}
                          <span style={{ position: "relative", bottom: "4px" }}>
                            <form method="get" action={downloadUrl}>
                              <button type="submit">
                                {this.state.resume.filename
                                  ? this.state.resume.filename
                                  : "no resumes"}
                              </button>
                            </form>
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
  isAuthenticated: state.auth.isAuthenticated,
  id: state.auth.id
});

export default connect(mapStateToProps, { sendInvitation, approve })(
  DreamerCollasCard
);
