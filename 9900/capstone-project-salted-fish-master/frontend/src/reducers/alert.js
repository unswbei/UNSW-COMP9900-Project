import { SET_ALERT, REMOVE_ALERT } from "../actions/actionTypes";

const initialState = [];

export default function (state = initialState, action) {
  switch (action.type) {
    case SET_ALERT:
      // immutable state
      return [...state, action.payload];
    case REMOVE_ALERT:
      console.log(action, state);
      return state.filter((alert) => alert.id !== action.payload);

    default:
      return state;
  }
}
