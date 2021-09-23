import { Map } from 'immutable';
import * as actionTypes from './constants';

const defaultState = Map({
  token: null,
  user: {},
  followings: [],
  likeList: {}
});

export default function reducer(state = defaultState, action) {
  switch (action.type) {
    case actionTypes.SET_TOKEN:
      return state.set("token", action.token);
    case actionTypes.SET_USER_DETAIL:
      return state.set("user", action.user);
    case actionTypes.SAVE_FOLLOWING_LIST:
      return state.set("followings", action.followings);
    case actionTypes.SAVE_LIKE_LIST:
      return state.set("likeList", action.likeList);
    default:
      return state;
  }
}
