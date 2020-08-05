import React, { Component } from "react";import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
// Import Materialize
import M from "materialize-css";
import { createProject } from "../../actions/projects";

class CreateProject extends Component {
  constructor(props) {
    super(props);
    this.handleonChange = this.handleonChange.bind(this);
    this.handleonSubmit = this.handleonSubmit.bind(this);
  }

  state = {
    title: "",
    category: null,
    description: "",
  };

  componentDidMount() {
    // Auto initialize all the materailize css!
    M.AutoInit();
  }

  handleonChange = (e) => {
    // get target element name
    this.setState({ [e.target.name]: e.target.value });
  };

  handleonSubmit = (e) => {
    e.preventDefault();

    const { title, category, description } = this.state;

    this.props.createProject({ title, category, description });
  };

  render() {
    const { isAuthenticated, flag } = this.props;
    if (!isAuthenticated) return <Redirect to="/login" />;
    // console.log(flag);
    if (flag === "create success") return <Redirect to="/projects" />;
    // console.log(this.props.isAuthenticated);

    return (
      <div className="container" style={{ marginTop: "50px" }}>
        <div className="card z-depth-6">
          <div className="row" style={{ paddingTop: "20px" }}>
            <form className="col s12" onSubmit={(e) => this.handleonSubmit(e)}>
              <div className="row">
                <div className=" col s12">
                  <label htmlFor="title">Project Title</label>
                  <input
                    placeholder="enter your project's title"
                    type="text"
                    name="title"
                    onChange={(e) => this.handleonChange(e)}
                    required
                  />

                </div>
              </div>

              <div className="row">
                <div className="input-field col s12">
                  <select
                    name="category"
                    onChange={(e) => this.handleonChange(e)}
                    placeholder="please choose the realated fields"
                  >
                    <option value="" disabled selected>
                      Choose your option
                    </option>
                    <option value="1">All other</option>
                    <option value="2">A web based application</option>
                    <option value="3">A desktop application</option>
                    <option value="4">A mobile application</option>
                    <option value="5">
                      A library for other project to reference
                    </option>
                    <option value="6">
                      A modification to existing platform
                    </option>
                    <option value="7">A research oriented project</option>
                  </select>
                  <label>Project catagory</label>
                </div>
              </div>

              <div className="row">
                <div className="col s12">
                  <label htmlFor="description">Describe your project!</label>
                  <textarea
                    placeholder="describe your project details not more than 140 words"
                    className="materialize-textarea"
                    length="140"
                    name="description"
                    onChange={(e) => this.handleonChange(e)}
                    required
                  ></textarea>

                </div>
              </div>
              <div className="row">
                <input
                  type="submit"
                  className="btn right blue-grey lighten-1"
                  value="Create"
                  style={{ marginRight: "20px" }}
                />
              </div>
            </form>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  isAuthenticated: state.auth.isAuthenticated,
  flag: state.project.flag,
});

export default connect(mapStateToProps, { createProject })(CreateProject);
