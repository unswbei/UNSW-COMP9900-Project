import React, { Component } from "react";
import CommentList from "./ReactCommentList";
import CommentForm from "./ReactCommentForm";
import M from "materialize-css";
import axios from "axios";

class ReactApp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      comments: [],
    };

    this.addComment = this.addComment.bind(this);
  }

  async componentDidMount() {
    // loading
    M.AutoInit();
    const a = localStorage.getItem("token");
    this.setState({ loading: true });
    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };
    const url = "/project/" + this.props.id + "/discussions";
    const res = await axios.get(url, config);
    console.log(res);
    this.setState({
      comments: res.data.discussion_info,
    });
  }

  /**
   * Add new comment
   * @param {Object} comment
   */
  addComment(comment) {
    console.log(comment);
    this.setState({
      comments: [comment, ...this.state.comments],
    });
    console.log(this.state.comments);
  }

  render() {
    return (
      <div className="card-panel light shadow">
        <h4 style={{ fontFamily: "Ubuntu" }}>comment section</h4>
        <CommentForm addComment={this.addComment} id={this.props.id} />
        <CommentList
          comments={this.state.comments}
          addComment={this.addComment}
          id={this.props.id}
        />
      </div>
    );
  }
}

export default ReactApp;
