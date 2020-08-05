import React, { useState } from "react";
import { Link } from "react-router-dom";

function Test() {
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
    console.log(fields);
  }

  function handleAdd() {
    const values = [...fields];
    values.push({ value: null });
    setFields(values);
  }

  function handleRemove(i) {
    const values = [...fields];
    values.splice(i, 1);
    setFields(values);
  }

  return (
    <div className="App">
      <h1>Hello CodeSandbox</h1>

      <button type="button" onClick={() => handleAdd()}>
        +
      </button>

      {fields.map((field, idx) => {
        return (
          <div>
            <div key={`${field}-${idx}`}>
              <div>
                <label className="left">Please enter your experience</label>
                <input
                  type="number"
                  placeholder="enter one number"
                  // onChange 响应到value里
                  onChange={(e) => handleValueChange(idx, e)}
                  min="0"
                  required
                />
              </div>
              <div>
                <label className="left">
                  Please choose your current job/major
                </label>
                <select
                  className="browser-default"
                  onChange={(e) => handleSkillChange(idx, e)}
                >
                  <option value="" disabled>
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
              <button type="button" onClick={() => handleRemove(idx)}>
                X
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
export default Test;
