import { SET_ALERT, REMOVE_ALERT } from "./actionTypes";
import { v4 as uuid } from "uuid";

export const setAlert = (msg) => (dispatch) => {
  // generate unique id
  const id = uuid();
  console.log(id);
  // dispatch to reducer
  // console.log(msg);
  dispatch({
    type: SET_ALERT,
    payload: { msg, id },
  });
  // disappear after 5s trigger remove alert
  setTimeout(() => dispatch({ type: REMOVE_ALERT, payload: id }), 6000);
};
