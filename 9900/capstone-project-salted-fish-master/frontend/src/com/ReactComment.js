import React from "react";

import CommentForm from "./ReactCommentForm";
import { connect } from "react-redux";
import moment from "moment-timezone";
import { setAlert } from "../actions/alert";

class ReactComment extends React.Component {
  constructor(props) {
    super();
    this.hideReply = this.hideReply.bind(this);
  }
  state = {
    reply: false,
  };

  hideReply() {
    this.setState({ reply: false });
    this.props.setAlert("messages reply success");
  }

  render() {
    const url =
      "https://api.adorable.io/avatars/48/" +
      this.props.comment.author_name +
      "@adorable.io.png";

    console.log(this.props.comment.create_time);

    return (
      <ul className="collection">
        <li className="collection-item avatar">
          <img src={url} alt="" className="circle" />
          <span className="title blue-text right">
            #{this.props.comment.discussion_id}
          </span>

          <span className="title blue-text">
            {this.props.comment.author_name}{" "}
            {this.props.comment.parent_id !== null &&
            this.props.comment.parent_id !== 0 ? (
              <span>reply to #{this.props.comment.parent_id}</span>
            ) : (
              ""
            )}
          </span>

          {this.props.comment.is_owner === "No" ? (
            ""
          ) : (
            <span className="right">owner</span>
          )}
          <span style={{ marginLeft: "5px" }}>
            {moment(this.props.comment.create_time).fromNow()}
          </span>
          <div>
            <div>{this.props.comment.content}</div>

            <button
              style={{ marginRight: "10px" }}
              onClick={(e) => {
                this.setState({ reply: true });
              }}
              className="btn-small right "
            >
              <i className="material-icons left" style={{ marginRight: "1px" }}>
                reply
              </i>
              reply
            </button>
          </div>
          {this.state.reply ? (
            <CommentForm
              addComment={this.props.addComment}
              id={this.props.id}
              hideReply={this.hideReply}
              comment={this.props.comment}
            />
          ) : (
            ""
          )}
        </li>
      </ul>
    );
  }
}

export default connect(null, { setAlert })(ReactComment);
