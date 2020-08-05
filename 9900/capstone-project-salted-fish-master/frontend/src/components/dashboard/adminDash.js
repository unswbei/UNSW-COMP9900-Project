import React, { Component } from "react";
import { connect } from "react-redux";
import { getProject, searchProject } from "../../actions/projects";
import M from "materialize-css";
import AdminEachProject from "../projects/adminEachProject";
import axios from "axios";

class AdminDash extends Component {

  constructor(props) {
    super(props);
  }

  state = {
    activeProjects:[],
    hiddenProjects:[],
    modifiedProjects:[],
  };


  componentWillMount() {
    this.props.getProject();
  }



  async componentDidMount() {
    // Auto initialize all the materailize css!
    M.AutoInit();
    // Auto initialize all the materailize css!
    const a = localStorage.getItem("token");

    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };

    const res1 = await axios.get("/admin/active_projects", config);
    this.setState({ activeProjects: res1.data.active_projects });
    console.log(res1.data)
    const res2 = await axios.get("/admin/hidden_projects", config);
    this.setState({ hiddenProjects: res2.data.hidden_projects});

    const res3 = await axios.get("/admin/modified_after_hidden_projects", config);
    this.setState({ modifiedProjects: res3.data.modified_after_hidden_projects});

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
      <div>
        <div className="container" style={{ marginTop: "20px" }}>

          <div className="divider"></div>
          <div className="section">
            <h5>Modified Projects</h5>
            <div className="flexLayout">
              {/*{this.props.ProjectLists.map((each, index) => {*/}
              {this.state.modifiedProjects&&this.state.modifiedProjects.map((each, index) => {
                // console.log("Active projects",this.state.activeProjects)
                // console.log("All projects",this.props.ProjectLists)
                return (
                    <div>
                      <AdminEachProject
                          title={each.title}
                          category={each.category}
                          description={each.description}
                          isHidden={each.is_hidden}
                          id={each.id}
                      />
                    </div>
                );
              })}
            </div>
          </div>

          <div className="divider"></div>
          <div className="section">
            <h5>Hidden Projects</h5>
            <div className="flexLayout">
              {/*{this.props.ProjectLists.map((each, index) => {*/}
              {this.state.hiddenProjects&&this.state.hiddenProjects.map((each, index) => {
                // console.log("Active projects",this.state.activeProjects)
                // console.log("All projects",this.props.ProjectLists)
                return (
                    <div>
                      <AdminEachProject
                          title={each.title}
                          category={each.category}
                          description={each.description}
                          isHidden={each.is_hidden}
                          id={each.id}
                      />
                    </div>
                );
              })}
            </div>
          </div>

          <div className="divider"></div>
          <div className="section">
            <h5>Active Projects</h5>
            <div className="flexLayout">
              {/*{this.props.ProjectLists.map((each, index) => {*/}
              {this.state.activeProjects&&this.state.activeProjects.map((each, index) => {
                // console.log("Active projects",this.state.activeProjects)
                // console.log("All projects",this.props.ProjectLists)
                return (
                    <div>
                      <AdminEachProject
                          title={each.title}
                          category={each.category}
                          description={each.description}
                          isHidden={each.is_hidden}
                          id={each.id}
                      />
                    </div>
                );
              })}
            </div>
          </div>

        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  isAuthenticated: state.auth.isAuthenticated,
  ProjectLists: state.project.ProjectLists,
});

export default connect(mapStateToProps, { getProject, searchProject })(
  AdminDash
);
