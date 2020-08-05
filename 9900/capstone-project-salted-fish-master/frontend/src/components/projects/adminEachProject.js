import React, { Component as component, Component, useCallback } from "react";
import { connect } from "react-redux";
import {Link, Redirect} from "react-router-dom";
import M from "materialize-css";
import axios from "axios";
import { Button, Modal } from "react-materialize";
import { loginUser } from "../../actions/auth";
import { setAlert } from "../../actions/alert";

class AdminEachProject extends Component {
  state = { isHidden: this.props.isHidden, hideReason: "" };

  handleonChange = (e) => {
    // get target element name
    this.setState({ [e.target.name]: e.target.value });
  };

  async handleonSubmit(e) {
    e.preventDefault();
    const a = localStorage.getItem("token");

    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };

    console.log(this.state.hideReason);
    const url = "/project/" + this.props.id + "/hide";

    const hidden_reason = this.state.hideReason;
    const body = JSON.stringify({
      hidden_reason,
    });

    const res = await axios.post(url, body, config);
    console.log(res);
    alert(res.data.message);
    this.setState({ isHidden: 1 });
  }

  async handleReveal() {
    // api call
    const a = localStorage.getItem("token");
    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };
    const url = "/project/" + this.props.id + "/unhide";
    const res = await axios.get(url, config);
    alert(res.data.message);
    this.setState({ isHidden: 0 });
  }

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
            {this.props.title}
            <i className="material-icons right">more_vert</i>
          </span>
          <p className="truncate">
            Category: {this.props.category}
          </p>
          <p className="truncate">Description: {this.props.description}</p>
        </div>
        <div className="card-action">
          {this.state.isHidden == 0 ? (
            <Modal
              trigger={
                <Button
                  className="waves-effect waves-light btn-small"
                  style={{ marginRight: "5px" }}
                >
                  hide
                </Button>
              }
            >
              <form
                className="col s12"
                onSubmit={(e) => this.handleonSubmit(e)}
              >
                <div>
                  <label htmlFor="title">Hide reason</label>
                  <input
                    placeholder="Tell user why you hide this project to the public"
                    type="text"
                    name="hideReason"
                    onChange={(e) => this.handleonChange(e)}
                    required
                  />
                </div>
                <input
                  type="submit"
                  className="btn-small left"
                  value="hide"
                  style={{ marginTop: "38px" }}
                />
              </form>
            </Modal>
          ) : (
            <button
              className=" btn-small"
              style={{ marginRight: "5px" }}
              onClick={(e) => this.handleReveal(e)}
            >
              reveal
            </button>
          )}
            <Link
                to={"/projects/" + this.props.id}
                className="btn-small"
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

export default connect(null, { setAlert })(AdminEachProject);
