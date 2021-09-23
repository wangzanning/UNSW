import { Map } from 'immutable';
import * as actionTypes from './constants';

const defaultState = Map({
  token: ""
});

export default function reducer(state = defaultState, action) {
  switch (action.type) {
    case actionTypes.SET_TOKEN:
      return state.set("token", action.setToken);
    default:
      return state;
  }
}
