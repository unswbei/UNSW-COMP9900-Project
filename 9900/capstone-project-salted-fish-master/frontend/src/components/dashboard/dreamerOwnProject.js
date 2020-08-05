import React from "react";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import axios from "axios";

import { setAlert } from "../../actions/alert";

class DreamerOwnProject extends React.Component {
  constructor() {
    super();

    this.handleFinish = this.handleFinish.bind(this);
  }

  async handleFinish(id) {
    const a = localStorage.getItem("token");
    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };
    id = Number(id);
    try {
      const res = await axios.get("/project/" + id + "/finish", config);
      this.props.setAlert(res.data.message);
    } catch (err) {
      // error -> dispatch setAlert to reducers
      this.props.setAlert(err.response.data.message);
    }
  }

  render() {
    if (!this.props.isAuthenticated) {
      return <Redirect to="/login" />;
    }

    const url =
      "https://source.unsplash.com/collection/" +
      Math.floor(Math.random() * 500) +
      "/800x600";

    const projectDetails = "/projects/" + this.props.id;
    const addRoleUrl = "/project/" + this.props.id + "/role";
    const id = this.props.id;
    const change = "/change/" + id;
    return (
      <div className="card medium event-card">
        <div className="card-image">
          <img src={url} alt="banner" />
        </div>
        <div className="card-content">
          <div className="card-title">
            {this.props.status == 9 ? (
              <b style={{ textDecoration: "line-through" }}>
                {this.props.title}
              </b>
            ) : (
              <b>{this.props.title}</b>
            )}
              {this.props.owner==this.props.myId?
                  <div className="right">

                      {this.props.status==9? <button disabled={true}
                                                     className="red btn-small disabled"
                                                     style={{ marginRight: "5px" }}
                      >
                          Change
                      </button>: <Link to={change}><button
                          className="red btn-small"
                          style={{ marginRight: "5px" }}
                      >
                          Change
                      </button></Link>}


                      {this.props.status==9? <button disabled={true}
                                                     className="red btn-small disabled"
                                                     onClick={() => this.handleFinish(id)}
                      >
                          Finish
                      </button>: <button
                          className="red btn-small"
                          onClick={() => this.handleFinish(id)}
                      >
                          Finish
                      </button>}

                  </div>: <span className="right" style={{fontSize: 15}}> Followed Project</span>}

          </div>

          <div className="left" style={{ marginTop: "15px" }}>
            <p>
              <Link to={projectDetails}>View Details</Link>
            </p>
            <p>create project time: {this.props.create_time.split(" ")[0]}</p>
          </div>
          <div className="right-align" style={{ marginTop: "20px" }}>
              {this.props.owner==this.props.myId?
                  <div>
                      {this.props.status==9? <button disabled={true} className="waves-effect waves-light btn-small disabled">
                      <i className="material-icons left">add</i>Add roles
                  </button>:<Link to={addRoleUrl}><button className="waves-effect waves-light btn-small">
                      <i className="material-icons left">add</i>Add roles
                  </button> </Link>}</div>: <div><br/></div>}



            <p>
              <b>category:</b> {this.props.category}
            </p>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  isAuthenticated: state.auth.isAuthenticated,
    myId: state.auth.id,
  ProjectLists: state.project.CollaProjectLists,
});

export default connect(mapStateToProps, { setAlert })(DreamerOwnProject);
