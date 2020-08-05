import axios from "axios";
import { setAlert } from "./alert";
import {
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  REGISTER_DISAPPEAR,
} from "./actionTypes";

// register user
export const registerDreamer = ({
  name,
  email,
  password,
  repeat_password,
  phone_no,
}) => async (dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
    },
  };

  const body = JSON.stringify({
    name,
    email,
    password,
    repeat_password,
    phone_no,
  });
  console.log(body);

  try {
    const res = await axios.post("/dreamer/register", body, config);
    console.log(res.data);

    dispatch(setAlert(res.data.message));

    dispatch({
      type: REGISTER_SUCCESS,
      payload: res.data,
    });

    setTimeout(() => dispatch({ type: REGISTER_DISAPPEAR }), 100);
  } catch (err) {
    // error -> dispatch setAlert to reducers
    console.log(err.response.data);
    const errors = err.response.data.message;
    dispatch(setAlert(errors));

    dispatch({
      type: REGISTER_FAIL,
    });
  }
};

// register Colla
export const registerColla = ({
  name,
  email,
  phone_no,
  password,
  repeat_password,
  education,
  skills,
  experience,
}) => async (dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
    },
  };

  // change to defalult type
  education = Number(education);

  const body = JSON.stringify({
    name,
    email,
    phone_no,
    password,
    repeat_password,
    education,
    skills,
    experience,
  });
  console.log(body);

  try {
    const res = await axios.post("/collaborator/register", body, config);
    console.log(res.data);

    dispatch(setAlert(res.data.message));

    // good register
    dispatch({
      type: REGISTER_SUCCESS,
      payload: res.data,
    });

    setTimeout(() => dispatch({ type: REGISTER_DISAPPEAR }), 1000);
  } catch (err) {
    console.log(err.response.data);
    const errors = err.response.data.message;

    // error -> dispatch setAlert to reducers
    dispatch(setAlert(errors));
    // bad register
    dispatch({
      type: REGISTER_FAIL,
    });
  }
};

// login user
export const loginUser = (email, password, role) => async (dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
    },
  };

  const body = JSON.stringify({
    password,
    email,
    role,
  });
  console.log(body);

  try {
    const res = await axios.post("/login", body, config);
    console.log(res.data);

    dispatch({
      type: LOGIN_SUCCESS,
      payload: { ...res.data, role },
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    console.log(err.response.data);
    const errors = err.response.data.message;
    dispatch(setAlert(errors));

    dispatch({
      type: LOGIN_FAIL,
    });
  }
};

// sign out
export const logOut = () => (dispatch) => {
  dispatch({ type: LOGOUT });
};
