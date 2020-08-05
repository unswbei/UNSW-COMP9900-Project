import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { postProjectRole } from "../../actions/projects";
import { Modal,Button } from "react-materialize";
import M from "materialize-css";
import GetApplications from "./getApplications";

const AddRoleProject = (props) => {
  const [flag, setFlag] = useState(0);

  useEffect(() => {
    M.AutoInit();
  });

  const [fields, setFields] = useState([
    {
      title: "",
      amount: 0,
      skill: "",
      experience: 0,
      education: 0,
      general_enquiry: "",
    },
  ]);

  function handleEnquiryChange(i, event) {
    const values = [...fields];
    values[i].general_enquiry = event.target.value;
    setFields(values);
  }

  function handleTitleChange(i, event) {
    const values = [...fields];
    values[i].title = event.target.value;
    setFields(values);
  }

  function handleAmountChange(i, event) {
    const values = [...fields];
    values[i].amount = event.target.value;
    setFields(values);
  }

  function handleEducationChange(i, event) {
    const values = [...fields];
    values[i].education = event.target.value;
    setFields(values);
  }

  function handleExperienceChange(i, event) {
    const values = [...fields];
    values[i].experience = event.target.value;
    setFields(values);
  }

  function handleSkillChange(event, j) {
    const values = [...fields];
    console.log(event.target.options);
    var options = event.target.options;
    console.log(j);
    var value = [];
    for (var i = 0, l = options.length; i < l; i++) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }

    // console.log(values[0].skill);
    value = value.join(",");

    values[j].skill = value;
    console.log(values);
    setFields(values);
  }

  const id = props.match.params.id;
  function handleAdd(e) {
    e.preventDefault();

    const {
      title,
      amount,
      skill,
      experience,
      education,
      general_enquiry,
    } = fields[fields.length - 1];

    props.postProjectRole({
      title,
      amount,
      skill,
      experience,
      education,
      general_enquiry,
      id,
    });

    const values = [...fields];
    values.push({
      title: "",
      amount: 0,
      skill: "",
      experience: 0,
      education: 0,
      general_enquiry: "",
    });
    console.log(values);
    setFields(values);
  }
  
  function handleFlag(e) {
    const {
      title,
      amount,
      skill,
      experience,
      education,
      general_enquiry,
    } = fields[fields.length - 1];
    
    let fi = fields[fields.length - 1];
    
    if (fi.title == "" || fi.amount == 0 || fi.skill == "" || fi.experience == 0 || fi.education == 0 || fi.general_enquiry == "") {
      console.log("finish with last one not valid, skip");
    } else {
      props.postProjectRole({
        title,
        amount,
        skill,
        experience,
        education,
        general_enquiry,
        id,
      });
    }
    
    const Flag = 1;
    setFlag(Flag);
  }

  if (flag === 1) {
    
    return <Redirect to="/dashboard" />;
  }

  return (
    <div className="container">
      <div className="valign-wrapper" style={{ marginTop: "50px" }}>
        <div className="row center">
          <p>THIS IS YOUR FIRST {fields.length} ROLES</p>
          <div className="col s12 m10 l12 card-panel z-depth-6">
            <form onSubmit={(e) => handleAdd(e)}>
              {fields.map((field, idx) => {
                return (
                  <div>
                    <div key={idx}>
                      <div className="row">
                        <div className="col l4">
                          <label className="left">Role's Title</label>
                          <input
                            type="text"
                            placeholder="enter roles title of your project"
                            onChange={(e) => handleTitleChange(idx, e)}
                            min="0"
                            required
                          />
                        </div>

                        <div className="col l4">
                          <label className="left">Role's Amount</label>
                          <input
                            type="number"
                            placeholder="enter roles amount of your project"
                            onChange={(e) => handleAmountChange(idx, e)}
                            min="0"
                            required
                          />
                        </div>

                        <div className="col l4">
                          <label className="left">Role's General_enquiry</label>
                          <input
                            type="text"
                            placeholder="enter the basic skills you wish your collabortors have"
                            onChange={(e) => handleEnquiryChange(idx, e)}
                            min="0"
                            required
                          />
                        </div>
                      </div>
                      <div className="row">
                        <div className="col l4">
                          <label className="left">Role's education level</label>
                          <select
                            className="browser-default"
                            onChange={(e) => handleEducationChange(idx, e)}
                            required
                            placeholder="enter the role's education level of your project"
                          >
                            <option selected disabled>
                              Choose your option
                            </option>
                            <option value="1">Other</option>
                            <option value="2">Bachelor</option>
                            <option value="3">Master</option>
                            <option value="4">Phd</option>
                          </select>
                        </div>

                        <div className="input-field col l4">
                          <select
                            required
                            multiple
                            onChange={(e) => handleSkillChange(e, idx)}
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
                              return (
                                <option value={index+1} key={index} >
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
                            placeholder="enter the minimal skill experience of your role"
                            onChange={(e) => handleExperienceChange(idx, e)}
                            min="0"
                            required
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}

              <br></br>
              <input
                type="submit"
                className="btn btn-primary"
                value="ADD ONE ROLE"
                style={{ marginBottom: "10px" }}
              />

              {/*There is bug with this Modal*/}
              {/*Close button does not work*/}

                <button
                    className="btn-small right"
                    style={{ marginTop: "10px" }}
                    onClick={(e) => handleFlag(e)}
                >
                  Finish
                </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  flag: state.auth.flag,
});

export default connect(null, { postProjectRole })(AddRoleProject);
