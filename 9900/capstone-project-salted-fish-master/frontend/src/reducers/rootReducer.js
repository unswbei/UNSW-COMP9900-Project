import { combineReducers } from "redux";
import alert from "./alert";
import auth from "./auth";
import project from "./project";

const rootReducer = combineReducers({
  alert,
  auth,
  project,
});

export default rootReducer;
