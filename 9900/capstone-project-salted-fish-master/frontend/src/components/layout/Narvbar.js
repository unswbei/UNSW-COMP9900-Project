import React from "react";
import { Link } from "react-router-dom";
import BeforeAuthNarvbar from "./BeforeAuthNarvbar";
import AfterAuthNarvbar from "./AfterAuthNarvbar";
import { connect } from "react-redux";

const Narvbar = (props) => {
  const { isAuthenticated } = props;

  return (
    <div>{isAuthenticated ? <AfterAuthNarvbar /> : <BeforeAuthNarvbar />}</div>
  );
};

const mapStateToProps = (state) => ({
  isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, null)(Narvbar);
