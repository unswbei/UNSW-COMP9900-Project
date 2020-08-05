import React, { Component } from "react";
import axios from "axios";
import { connect } from "react-redux";

class CommentForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      error: "",
      comment: {
        content: "",
      },
    };

    // bind context to methods
    this.handleFieldChange = this.handleFieldChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  /**
   * Handle form input field changes & update the state
   */
  handleFieldChange = (event) => {
    const { value, name } = event.target;

    this.setState({
      ...this.state,
      comment: {
        ...this.state.comment,
        [name]: value,
      },
    });
  };

  /**
   * Form submit handler
   */
  async onSubmit(e) {
    // prevent default form submission
    e.preventDefault();

    if (!this.isFormValid()) {
      this.setState({ error: "Please input your message" });
      return;
    }
    try {
      this.props.hideReply();
    } catch (e) {}
    // loading status and clear error
    this.setState({ error: "" });
    // persist the comments on server
    let { comment } = this.state;
    console.log(comment);
    const a = localStorage.getItem("token");
    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };

    const discuss_content = comment.content;
    try {
      const parent_id = this.props.comment.discussion_id;
      const body = JSON.stringify({
        parent_id,
        discuss_content: discuss_content,
      });
      console.log(body);
      const url = "/project/" + this.props.id + "/discussion";
      const res = await axios.post(url, body, config);
      const discussion_id = res.data.discussion_id;
      console.log(res);
      const author_name = this.props.name;
      comment = { ...comment, author_name, discussion_id, parent_id };
      this.props.addComment(comment);
    } catch (e) {
      const parent_id = 0;
      const body = JSON.stringify({
        parent_id,
        discuss_content: discuss_content,
      });

      const url = "/project/" + this.props.id + "/discussion";
      const res = await axios.post(url, body, config);
      console.log(res.data);
      const discussion_id = res.data.discussion_id;
      const author_name = this.props.name;
      const create_time = res.data.post_time;
      const is_owner = res.data.post_by;
      comment = {
        ...comment,
        author_name,
        parent_id,
        discussion_id,
        is_owner,
        create_time,
      };
      this.props.addComment(comment);
    }

    // this.setState({
    //   comment: { ...comment, content: discuss_content },
    // });
  }

  /**
   * Simple validation
   */
  isFormValid() {
    return this.state.comment.name !== "" && this.state.comment.content !== "";
  }

  render() {
    return (
      <React.Fragment>
        <div className="comment-input">
          <div className="input-field">
            <form onSubmit={(e) => this.onSubmit(e)}>
              <div className="comment-field-input">
                <textarea
                  onChange={this.handleFieldChange}
                  value={this.state.comment.content}
                  className="materialize-textarea"
                  placeholder="Your Comment"
                  name="content"
                  rows="5"
                />
              </div>

              <div>
                <button
                  disabled={this.state.loading}
                  className="btn-small blue-grey lighten-1 right"
                  style={{ marginBottom: "10px" }}
                >
                  Comment &#10148;
                </button>
              </div>
            </form>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

const mapStateToProps = (state) => ({
  name: state.auth.name,
});

export default connect(mapStateToProps, null)(CommentForm);
