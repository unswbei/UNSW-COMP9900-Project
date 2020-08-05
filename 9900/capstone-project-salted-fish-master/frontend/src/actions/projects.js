import axios from "axios";
import { setAlert } from "./alert";
import {
  CREATE_PROJECT_FAIL,
  CREATE_PROJECT_SUCCESS,
  GET_PROJECT_LIST,
  UNDO_FLAG,
  SEARCH_PROJECT_LIST,
  POST_PROJECT_ROLE,
  POST_PROJECT_ROLE_FAIL,
  CHANGE_PROJECT_ROLE,
  CHANGE_PROJECT_ROLE_FAIL,
  SEND_INVITATION,
  APPLY_ROLE,
  APPPROVE_APPLICATION,
  DECLINE_APPLICATION,
  GET_COLLA_PROJECT_LIST,
  SEARCH_COLLA_PROJECT_LIST,
  ACCEPT_INVITATION,
  DECLINE_INVITATION,
  UPLOAD_RESUME,
  FINISH_PROJECTS,
  CHANGE_PROJECTS,
  UNDO_CHANGE,
  GET_ACTIVE_PROJECT_LIST,
} from "./actionTypes";

// createProject
export const createProject = ({ title, category, description }) => async (
  dispatch
) => {
  const a = localStorage.getItem("token");

  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };
  category = Number(category) - 1;
  console.log(category, typeof category);
  const body = JSON.stringify({
    title,
    category,
    description,
  });

  try {
    const res = await axios.post("/project", body, config);
    console.log(res.data);

    dispatch(setAlert(res.data.message));

    dispatch({
      type: CREATE_PROJECT_SUCCESS,
      payload: res.data.project_id,
    });

    setTimeout(() => dispatch({ type: UNDO_FLAG }), 100);
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));

    dispatch({
      type: CREATE_PROJECT_FAIL,
    });
  }
};

// getProject list
export const getProject = () => async (dispatch) => {
  try {
    const res = await axios.get("/projects");
    console.log(res.data);

    dispatch({
      type: GET_PROJECT_LIST,
      payload: res.data,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    console.log(err.response);
  }
};


// search
export const searchProject = ({
  description,
  category,
  order_by,
  sorting,
}) => async (dispatch) => {
  category = Number(category) - 1;
  try {
    const res = await axios.get(
      "/projects?description=" +
        description +
        "&category=" +
        category +
        "&order_by=" +
        order_by +
        "&sorting=" +
        sorting
    );
    console.log(res.data);

    dispatch(setAlert(res.data.message));
    dispatch({
      type: SEARCH_PROJECT_LIST,
      payload: res.data,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    console.log(err.response);
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// postProjectRole list
export const postProjectRole = ({
  title,
  amount,
  skill,
  experience,
  education,
  general_enquiry,
  id,
}) => async (dispatch) => {
  const a = localStorage.getItem("token");

  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };

  amount = Number(amount);
  experience = Number(experience);
  education = Number(education);
  id = Number(id);

  const body = JSON.stringify({
    title,
    amount,
    skill,
    experience,
    education,
    general_enquiry,
  });
  console.log(body);

  try {
    // need to change

    const res = await axios.post("/project/" + id + "/role", body, config);
    console.log(res.data);

    dispatch(setAlert(res.data.message));

    dispatch({
      type: POST_PROJECT_ROLE,
      payload: res.data,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));

    dispatch({
      type: POST_PROJECT_ROLE_FAIL,
    });
  }
};

// postProjectRole list
export const changeProjectRole = ({
  title,
  amount,
  skill,
  experience,
  education,
  general_enquiry,
  pid,
  rid,
}) => async (dispatch) => {
  const a = localStorage.getItem("token");

  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };

  amount = Number(amount);
  experience = Number(experience);
  education = Number(education);
  pid = Number(pid);
  rid = Number(rid);

  const body = JSON.stringify({
    title,
    amount,
    skill,
    experience,
    education,
    general_enquiry,
  });
  console.log(body);

  try {
    // need to change
    const res = await axios.patch(
      "/project/" + pid + "/role/" + rid,
      body,
      config
    );
    console.log(res.data);

    dispatch(setAlert(res.data.message));

    dispatch({
      type: CHANGE_PROJECT_ROLE,
      payload: res.data,
    });
    setTimeout(() => dispatch({ type: CHANGE_PROJECT_ROLE_FAIL }), 100);
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));

    dispatch({
      type: CHANGE_PROJECT_ROLE_FAIL,
    });
  }
};

// sendInvitation
export const sendInvitation = ({ general_text, pid, rid, cid }) => async (
  dispatch
) => {
  const a = localStorage.getItem("token");

  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };

  const collaborator_id = Number(cid);
  const body = JSON.stringify({
    collaborator_id,
    general_text,
  });
  console.log(body);

  try {
    const url = "/project/" + pid + "/role/" + rid + "/invitation";
    const res = await axios.post(url, body, config);

    dispatch(setAlert(res.data.message));

    dispatch({
      type: SEND_INVITATION,
      payload: res.data.message,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// apply role
export const applyRole = ({ general_text, pid, rid }) => async (dispatch) => {
  const a = localStorage.getItem("token");
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };
  pid = Number(pid);
  rid = Number(rid);
  const body = JSON.stringify({
    general_text,
  });

  try {
    const url = "/project/" + pid + "/role/" + rid + "/appllication";
    console.log(url);
    const res = await axios.post(url, body, config);

    dispatch(setAlert(res.data.message));

    dispatch({
      type: APPLY_ROLE,
      payload: res.data.message,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// approve application
export const approve = ({ aid, rid, pid }) => async (dispatch) => {
  const a = localStorage.getItem("token");
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };
  aid = Number(aid);
  pid = Number(pid);
  rid = Number(rid);

  try {
    const url =
      "/project/" + pid + "/role/" + rid + "/application/" + aid + "/approve";
    console.log(url);
    const res = await axios.get(url, config);
    console.log(res.data);
    dispatch(setAlert(res.data.message));

    dispatch({
      type: APPPROVE_APPLICATION,
      payload: res.data.message,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};
// getCollaProject list
export const getCollaProject = () => async (dispatch) => {
  try {
    const a = localStorage.getItem("token");
    const config = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        "AUTH-KEY": a,
      },
    };
    const res = await axios.get("/collaborator/projects", config);
    console.log("COLLA!!!", res.data);

    dispatch({
      type: GET_COLLA_PROJECT_LIST,
      payload: res.data,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// approve application
export const decline = ({ aid, rid, pid }) => async (dispatch) => {
  const a = localStorage.getItem("token");
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };
  aid = Number(aid);
  pid = Number(pid);
  rid = Number(rid);

  try {
    const url =
      "/project/" + pid + "/role/" + rid + "/application/" + aid + "/decline";
    console.log(url);
    const res = await axios.get(url, config);
    console.log(res);
    dispatch(setAlert(res.data.message));

    dispatch({
      type: DECLINE_APPLICATION,
      payload: res.data.message,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// search
export const searchCollaProject = ({
  description,
  category,
  order_by,
  sorting,
}) => async (dispatch) => {
  category = Number(category) - 1;
  const a = localStorage.getItem("token");
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };
  try {
    const res = await axios.get(
      "/collaborator/projects?description=" +
        description +
        "&category=" +
        category +
        "&order_by=" +
        order_by +
        "&sorting=" +
        sorting,
        config
    );
    console.log(res.data);

    dispatch(setAlert(res.data.message));
    dispatch({
      type: SEARCH_COLLA_PROJECT_LIST,
      payload: res.data,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    console.log(err.response);
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// search
export const acceptInvitation = (url) => async (dispatch) => {
  const a = localStorage.getItem("token");
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };
  try {
    console.log(url);
    const res = await axios.get(url, config);
    console.log(res.data);

    dispatch(setAlert(res.data.message));
    dispatch({
      type: ACCEPT_INVITATION,
      payload: res.data,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    console.log(err.response);
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// declineInvitation
export const declineInvitation = (url) => async (dispatch) => {
  const a = localStorage.getItem("token");
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };
  try {
    const res = await axios.get(url, config);
    console.log(res.data);

    dispatch(setAlert(res.data.message));
    dispatch({
      type: DECLINE_INVITATION,
      payload: res.data,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    console.log(err.response);
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// declineInvitation
export const uploadResume = (file) => async (dispatch) => {
  const a = localStorage.getItem("token");
  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };

  const data = new FormData();
  data.append("file", file);
  console.log("!!!!!!", data);
  try {
    const res = await axios.post("/collaborator/resume", data, config);
    console.log(res.data);

    dispatch(setAlert(res.data.message));
    dispatch({
      type: UPLOAD_RESUME,
      payload: res.data,
    });
  } catch (err) {
    // error -> dispatch setAlert to reducers
    console.log(err.response);
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};

// declineInvitation
// export const finishProject = (id) => async (dispatch) => {
//   const a = localStorage.getItem("token");
//   const config = {
//     headers: {
//       "Content-Type": "application/json;charset=UTF-8",
//       "Access-Control-Allow-Origin": "*",
//       "AUTH-KEY": a,
//     },
//   };
//   id = Number(id);
//   try {
//     const res = await axios.get("/project/" + id + "/finish", config);
//     console.log(res);

//     dispatch(setAlert(res.data.message));
//     dispatch({
//       type: FINISH_PROJECTS,
//       payload: res.data,
//     });
//   } catch (err) {
//     // error -> dispatch setAlert to reducers
//     console.log(err.response);
//     const errors = err.response.data.message;
//     dispatch(setAlert(errors));
//   }
// };

// change project
export const changeProject = ({ title, category, description, id }) => async (
  dispatch
) => {
  const a = localStorage.getItem("token");

  const config = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
      "AUTH-KEY": a,
    },
  };
  const project_title = title;
  category = Number(category) - 1;
  const body = JSON.stringify({
    project_title,
    description,
    category,
  });
  const url = "/project/" + id;
  try {
    const res = await axios.patch(url, body, config);
    console.log(res.data);

    dispatch(setAlert(res.data.message));

    dispatch({
      type: CHANGE_PROJECTS,
      payload: res.data.message,
    });

    setTimeout(() => dispatch({ type: UNDO_CHANGE }), 100);
  } catch (err) {
    // error -> dispatch setAlert to reducers
    const errors = err.response.data.message;
    dispatch(setAlert(errors));
  }
};
