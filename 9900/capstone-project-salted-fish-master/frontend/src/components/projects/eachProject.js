import React, { Component } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import M from "materialize-css";
import { Link } from "react-router-dom";

class EachProject extends Component {
  render() {
    var categoryList = [
      "All other",
      "A web based application",
      "A desktop application",
      "A mobile application",
      "A library for other project to reference",
      "A modification to existing platform",
      "A research oriented project",
    ];
    return (
      <div
        className="card panel-up"
        style={{ width: "20em", marginLeft: "20px", marginRight: "10px" }}
      >
        <div className="card-image waves-effect waves-block waves-light"></div>
        <div className="card-content">
          <span className="card-title activator grey-text text-darken-4">
            {this.props.status === 9 ? (
              <span style={{ textDecoration: "line-through" }}>
                {this.props.title}
              </span>
            ) : (
              this.props.title
            )}
            <i className="material-icons right">more_vert</i>
          </span>
          <p className="truncate">
            Category: {categoryList[this.props.category]}
          </p>
          <p className="truncate">Description: {this.props.description}</p>
        </div>
        <div className="card-action">
          <Link
            to={"/projects/" + this.props.id}
            className="waves-effect waves-light btn-small blue-grey darken-1"
            style={{ marginRight: "5px" }}
          >
            More info
          </Link>
        </div>
        <div className="card-reveal">
          <span className="card-title grey-text text-darken-4">
            {this.props.title}
            <i className="material-icons right">close</i>
          </span>
          <p>Description: {this.props.description}</p>
        </div>
      </div>
    );
  }
}
export default EachProject;
