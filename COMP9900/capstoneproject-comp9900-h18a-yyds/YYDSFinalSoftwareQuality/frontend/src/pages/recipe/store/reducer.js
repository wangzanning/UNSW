import { Map } from 'immutable';
import * as actionTypes from './constants';

const defaultState = Map({
  data: {}
});

export default function reducer(state = defaultState, action) {
  switch (action.type) {
    case actionTypes.SET_RECIPE_DETIAL:
      return state.set("data", action.data);
    default:
      return state;
  }
}
