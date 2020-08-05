import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { setAlert } from "../../actions/alert";
import { registerColla } from "../../actions/auth";
import { Redirect } from "react-router-dom";
import M from "materialize-css";

const CollaRegis = ({ setAlert, registerColla, flag }) => {
  useEffect(() => {
    M.AutoInit();
  });

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    repeat_password: "",
    education: "",
  });

  const {
    name,
    email,
    password,
    repeat_password,
    phone_no,
    education,
  } = formData;

  const [fields, setFields] = useState([{ value: null, skill: null }]);

  function handleValueChange(i, event) {
    const values = [...fields];
    values[i].value = event.target.value;
    setFields(values);
  }

  function handleSkillChange(i, event) {
    const values = [...fields];
    values[i].skill = event.target.value;
    setFields(values);
  }

  function handleAdd() {
    const values = [...fields];
    values.push({ value: null });
    setFields(values);
  }

  // remove handler
  // function handleRemove(i) {
  //   const values = [...fields];
  //   values.splice(i, 1);
  //   setFields(values);
  // }

  const onChange = (e) => {
    // get target element name
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onSubmit = (e) => {
    e.preventDefault();
    var skillsArr = [];
    var experienceArr = [];

    for (var i of fields) {
      skillsArr.push(i.skill);
      experienceArr.push(i.value);
    }

    var skills = skillsArr.join(",");
    var experience = experienceArr.join(",");

    if (password !== repeat_password) {
      setAlert("Password does not match");
    } else {
      registerColla({
        name,
        email,
        phone_no,
        password,
        repeat_password,
        education,
        skills,
        experience,
      });
    }
  };

  // console.log(flag);
  if (flag === "register success") {
    return <Redirect to="/login" />;
  }

  return (
    <div>
      <form onSubmit={(e) => onSubmit(e)}>
        <div className="input-field">
          <input
            type="text"
            // placeholder="Name"
            name="name"
            value={name}
            onChange={(e) => onChange(e)}
            required
            id="name"
          />
          <label for="name">Name</label>
        </div>
        <div className="input-field">
          <input
            type="email"
            // placeholder="Email Address"
            name="email"
            value={email}
            onChange={(e) => onChange(e)}
            required
            id="email_address"
          />
          <label HtmlFor="email_address">Email Address</label>
        </div>
        <div className="input-field">
          <input
            type="text"
            // placeholder="Phone Number"
            name="phone_no"
            minLength="6"
            value={phone_no}
            onChange={(e) => onChange(e)}
            id="phone_number"
          />
          <label for="phone_number">Phone Number</label>
        </div>
        <div className="input-field">
          <input
            type="password"
            // placeholder="Password"
            name="password"
            minLength="8"
            value={password}
            onChange={(e) => onChange(e)}
            required
            id="password"
          />
          <label for="password">Password</label>
        </div>

        <div className="input-field">
          <input
            type="password"
            // placeholder="Confirm Password"
            name="repeat_password"
            minLength="8"
            value={repeat_password}
            onChange={(e) => onChange(e)}
            required
            id="confirm_password"
          />
          <label HtmlFor="confirm_password">Confirm Password</label>
        </div>

        <div className="input-field" style={{ marginBottom: "10px" }}>
          <select
            value={education}
            onChange={(e) => onChange(e)}
            name="education"
            id="education"
          >
            <option value="" disabled>
              Choose your option
            </option>
            <option value="1">Other</option>
            <option value="2">Bachelor</option>
            <option value="3">Master</option>
            <option value="4">Phd</option>
          </select>
          <label HtmlFor="education" className="left">
            Please select your highest education level
          </label>
        </div>

        {fields.map((field, idx) => {
          return (
            <div>
              <div key={`${field}-${idx}`}>
                <div style={{ marginBottom: "10px" }}>
                  <label HtmlFor="computer_skill" className="left">
                    Please choose your computer skill
                  </label>
                  <select
                    className="browser-default"
                    onChange={(e) => handleSkillChange(idx, e)}
                    id="computer_skill"
                  >
                    <option value="" disabled selected>
                      Choose your option
                    </option>
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
                        <option value={index} key={index}>
                          {ele}
                        </option>
                      );
                    })}
                  </select>
                </div>
                <div>
                  <label className="left">
                    How many years experience do you have in your field?
                  </label>
                  <input
                    type="number"
                    placeholder="enter one number"
                    onChange={(e) => handleValueChange(idx, e)}
                    min="0"
                    required
                  />
                </div>
              </div>
            </div>
          );
        })}
        <button
          type="btn-small"
          onClick={() => handleAdd()}
          style={{ marginBottom: "10px" }}
        >
          add one skill
        </button>

        <br></br>
        <input type="submit" className="btn btn-primary" value="Register" />
      </form>
    </div>
  );
};

const mapStateToProps = (state) => ({
  flag: state.auth.flag,
});

export default connect(mapStateToProps, { setAlert, registerColla })(
  CollaRegis
);
