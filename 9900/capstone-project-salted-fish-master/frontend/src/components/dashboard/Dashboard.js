import React from "react";
import CollaDash from "./collaDash";
import DreamerDash from "./dreamerDash";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

class Dashboard extends React.Component {
  render() {
    if (!this.props.isAuthenticated) {
      return <Redirect to="/login" />;
    }
    return (
      <div>
        {this.props.authRole === "Dreamer" ? <DreamerDash /> : <CollaDash />}
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  authRole: state.auth.role,
  isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, null)(Dashboard);
