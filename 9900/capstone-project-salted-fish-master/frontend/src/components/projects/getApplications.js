import React from "react";
import { Link } from "react-router-dom";
import axios from "axios";

class GetApplication extends React.Component {
  state = {
    a: [],
  };

  async componentWillMount() {
    const a = localStorage.getItem("token");

    const res = await axios.get(this.props.url_1, {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    });
    console.log("url", this.props.url_1);

    this.setState({ a: res.data.applications });
    console.log(this.state.a);
  }
  render() {
    console.log("applications",this.state.a)
    if (this.state.a.length == 0){
      return(
          <p>No applicaitons now.</p>
      )
    }else{
      return (
          <div>
            {this.state.a.map((each, index) => {
              const url =
                  "/project/" +
                  this.props.pid +
                  "/role/" +
                  this.props.rid +
                  "/collaborators/" +
                  each.application_id +
                  "/applications/"+each.id;
              console.log(each)
              if (each.apply_status == -1){
                return (
                    <div key={index} style={{ fontFamily: "Ubuntu" }}>
                      <Link to={url} style={{ marginRight: "10px" }}>
                        {each.name}
                      </Link>
                      want to apply for this role and leaves his messgae：
                      {each.general_text}
                    </div>
                );
              }
            })}
          </div>
      );
    }

  }
}

export default GetApplication;
