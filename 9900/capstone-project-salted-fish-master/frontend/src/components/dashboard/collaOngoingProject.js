import React from "react";
import { Link } from "react-router-dom";
import { Redirect } from "react-router-dom";
import { connect } from "react-redux";

class CollaOngoingProject extends React.Component {
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
          </div>
          <div className="left" style={{ marginTop: "15px" }}>
            <p>
              <Link to={projectDetails}>View Details</Link>
            </p>
            <p>create project time: {this.props.create_time.split(" ")[0]}</p>
          </div>
          <div className="right-align" style={{ marginTop: "20px" }}>
            <p>

              {this.props.follow ? <span>
                <i className="material-icons icon">favorite</i> Your followed project</span> : <span>Your role:{this.props.roleTitle}</span>}
            </p>
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
  authRole: state.auth.role,
  isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, null)(CollaOngoingProject);
