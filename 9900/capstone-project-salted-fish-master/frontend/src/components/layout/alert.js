import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";

// fetch alert
const Alert = ({ alerts }) =>
  alerts !== null &&
  alerts.length > 0 &&
  alerts.map((alert) => (
    <div
      key={alert.id}
      className="center light-green accent-2 container center"
      style={{
        position: "sticky",
        top: "5px",
        zIndex: 2,
      }}
    >
      {alert.msg}
    </div>
  ));

// Alert.PropTypes = {
//   alerts: PropTypes.array.isRequired,
// };

const mapStateToProps = (state) => ({
  alerts: state.alert,
});

export default connect(mapStateToProps)(Alert);
