import { Map } from 'immutable';
import * as actionTypes from './constants';

const defaultState = Map({
  searchQueries: {
    name: "",
    method: "",
    mealType: [],
    ingredients: []
  }
});

export default function reducer(state = defaultState, action) {
  switch (action.type) {
    case actionTypes.SET_SEARCH_QUERIES:
      return state.set("searchQueries", action.searchQueries);
    default:
      return state;
  }
}