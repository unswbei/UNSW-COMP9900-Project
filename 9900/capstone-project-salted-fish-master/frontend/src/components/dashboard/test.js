import React from "react";
import ReactDOM from "react-dom";
import { Modal, Button, Icon } from "react-materialize";

function Card() {
  const { headingText } = styles;

  return (
    <div className="container">
      <h2 style={headingText} className="flow-text">
        Modal React Demo
      </h2>
      <p className="flow-text">
        Learn how to use Materialize CSS framework in ReactJS
      </p>
      <Modal
        header="Modal Header"
        trigger={
          <Button waves="light">
            OR ME!<Icon right>insert_chart</Icon>
          </Button>
        }
      >
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </p>
      </Modal>
    </div>
  );
}

const styles = {
  headingText: {
    fontSize: 50,
    fontWeight: 300,
  },
};

export default Card;
