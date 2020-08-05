import React, { Component } from "react";
import axios from "axios";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
// Import Materialize
import M from "materialize-css";
import { changeProject } from "../../actions/projects";

class ChangeProject extends Component {
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

  async componentDidMount() {
    const role_url = "/project/" + this.props.match.params.id;
    const res = await axios.get(role_url);
    console.log(res.data);
    this.setState({title: res.data.title});
    this.setState({category: res.data.category});
    this.setState({description: res.data.description});
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
    const id = this.props.match.params.id;
    this.props.changeProject({ title, category, description, id });
  };

  render() {
    const { isAuthenticated, flag } = this.props;
    if (!isAuthenticated) return <Redirect to="/login" />;

    if (flag === "Patch success") return <Redirect to="/dashboard" />;

    return (
      <div className="container" style={{ marginTop: "50px" }}>
        <div className="card z-depth-6">
          <div className="row" style={{ paddingTop: "20px" }}>
            <form className="col s12" onSubmit={(e) => this.handleonSubmit(e)}>
              <div className="row">
                <div className="input-field col s12">
                  <input
                    value={this.state.title}
                    placeholder="enter your project's title"
                    type="text"
                    name="title"
                    onChange={(e) => this.handleonChange(e)}
                    required
                  />
                  <label htmlFor="title" className="active">Project Title</label>
                </div>
              </div>

              <div className="row">
                <div className="input-field col s12">
                  <select
                    name="category"
                    value={this.state.category}
                    onChange={(e) => this.handleonChange(e)}
                    placeholder="please choose the realated fields"
                  >
                    <option value="" disabled>
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
                <div className="input-field col s12">
                  <textarea
                    value={this.state.description}
                    placeholder="describe your project details not more than 140 words"
                    className="materialize-textarea"
                    length="140"
                    name="description"
                    onChange={(e) => this.handleonChange(e)}
                    required
                  ></textarea>
                  <label htmlFor="description" className="active">Describe your project!</label>
                </div>
              </div>
              <div className="row">
                <input
                  type="submit"
                  className="btn right"
                  value="Change"
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

export default connect(mapStateToProps, { changeProject })(ChangeProject);
