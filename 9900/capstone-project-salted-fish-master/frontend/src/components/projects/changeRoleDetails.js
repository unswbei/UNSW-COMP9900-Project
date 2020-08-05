import React from "react";
import axios from "axios";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { changeProjectRole } from "../../actions/projects";
import M from "materialize-css";

class ChangeRoleDetails extends React.Component {
  constructor(props) {
    super(props);
    this.handleSkillChange = this.handleSkillChange.bind(this);
  }

  state = {
    title: "",
    amount: 0,
    skill: "",
    skills: [],
    experience: 0,
    education: 0,
    general_enquiry: "",
  };

  async componentDidMount() {
    const role_url = "/project/" + this.props.match.params.pid + "/role/" + this.props.match.params.rid;
    const res = await axios.get(role_url);
    console.log(res.data);
    this.setState({title: res.data.title});
    this.setState({amount: res.data.amount});
    this.setState({skills: res.data.skill});
    this.setState({skill: res.data.skill.join(',')});
    this.setState({experience: res.data.experience});
    this.setState({education: res.data.education});
    this.setState({general_enquiry: res.data.general_enquiry});
    M.AutoInit();
  }
  handleonChange = (e) => {
    // get target element name
    this.setState({ [e.target.name]: e.target.value });
  };

  handleonSubmit = (e) => {
    e.preventDefault();
    const pid = this.props.match.params.pid;
    const rid = this.props.match.params.rid;

    const {
      title,
      amount,
      skill,
      experience,
      education,
      general_enquiry,
    } = this.state;
    console.log(this.state);

    this.props.changeProjectRole({
      title,
      amount,
      skill,
      experience,
      education,
      general_enquiry,
      pid,
      rid,
    });
  };

  handleSkillChange(event) {
    var options = event.target.options;
    var value = [];
    for (var i = 0, l = options.length; i < l; i++) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }

    // console.log(values[0].skill);
    value = value.join(",");
    console.log(value);
    this.setState({ skill: value });
  }

  render() {
    const url = "/projects/" + this.props.match.params.pid;
    if (this.props.hasChange) {
      return <Redirect to={url} />;
    }
    
    return (
      <div className="container">
        <div className="valign-wrapper" style={{ marginTop: "50px" }}>
          <div className="row center">
            <div className="col s12 m10 l12 card-panel z-depth-6">
              <form onSubmit={(e) => this.handleonSubmit(e)}>
                <div className="row">
                  <div className="col l4">
                    <label className="left">Role's Title</label>
                    <input
                      type="text"
                      value={this.state.title}
                      placeholder="enter roles title of your project"
                      name="title"
                      onChange={(e) => this.handleonChange(e)}
                      min="0"
                    />
                  </div>

                  <div className="col l4">
                    <label className="left">Role's Amount</label>
                    <input
                      type="number"
                      value={this.state.amount}
                      placeholder="enter roles amount of your project"
                      name="amount"
                      onChange={(e) => this.handleonChange(e)}
                      min="0"
                    />
                  </div>

                  <div className="col l4">
                    <label className="left">Role's General_enquiry</label>
                    <input
                      type="text"
                      value={this.state.general_enquiry}
                      placeholder="enter the basic skills you wish your collabortors have"
                      name=""
                      onChange={(e) => this.handleonChange(e)}
                      min="0"
                      name="general_enquiry"
                    />
                  </div>
                </div>
                <div className="row">
                  <div className="col l4">
                    <label className="left">Role's education level</label>
                    <select
                      required
                      className="browser-default"
                      onChange={(e) => this.handleonChange(e)}
                      placeholder="enter the role's education level of your project"
                      name="education"
                    >
                      <option selected disabled>
                        Choose your option
                      </option>
                      {["Other",
                        "Bachelor",
                        "Master",
                        "PhD",
                      ].map((element, index) => {
                        var is_select = "";
                        if (index + 1 === this.state.education) {
                          is_select = "selected";
                        }
                        return (
                          <option value={index + 1} selected={is_select}>{element}</option>
                        );
                      })}
                    </select>
                  </div>

                  <div className="input-field col l4">
                    <select
                      required
                      multiple
                      onChange={(e) => this.handleSkillChange(e)}
                      placeholder="role's skills of your project"
                    >
                    <option disabled>Select some skills</option>
                      {[
                        "Web Development",
                        "Java",
                        "Python",
                        "PHP",
                        "Script Language",
                        "Database Management",
                        "Computer Vision",
                        "Security Engineering",
                        "Testing",
                        "Algorithm Design",
                        "Operating System",
                        "Data Science",
                        "Human Computer Interaction",
                        "Deep Learning/Neural Network",
                        "Distribution System",
                      ].map((ele, index) => {
                        var is_select = "";
                        if (this.state.skill.includes(index + 1)) {
                          is_select = "selected";
                        }
                        return (
                          <option value={index + 1} key={index} selected={is_select}>
                            {ele}
                          </option>
                        );
                      })}
                    </select>
                    <label className="left">Role's Skills</label>
                  </div>

                  <div className="col l4">
                    <label className="left">Role's Experience</label>
                    <input
                      type="number"
                      value={this.state.experience}
                      placeholder="enter the minimal skill experience of your role"
                      onChange={(e) => this.handleonChange(e)}
                      min="0"
                      name="experience"
                    />
                  </div>
                </div>

                <input
                  type="submit"
                  className="btn btn-primary"
                  value="Change"
                  style={{ marginBottom: "10px" }}
                />
              </form>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  hasChange: state.project.hasChange,
});

export default connect(mapStateToProps, { changeProjectRole })(
  ChangeRoleDetails
);
