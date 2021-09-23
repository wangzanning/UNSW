import { combineReducers } from "redux";
import storageSession from 'redux-persist/lib/storage/session';

import { reducer as feedPageReducer } from "../pages/feed/store";
import { reducer as loginReducer } from "../pages/login/store";
import { reducer as signupReducer } from "../pages/signup/store";
import { reducer as recipeDetail } from '../pages/recipe/store';
import { reducer as searchReducer } from "../pages/search/store";
const appReducer = combineReducers({
  feed: feedPageReducer,
  login: loginReducer,
  signup: signupReducer,
  recipe: recipeDetail,
  search: searchReducer
});

const reducer = (state, action) => {
  if (action.type === 'USER_LOGOUT') {
    storageSession.removeItem('persist:root');
    state = undefined;
  }
  return appReducer(state, action);
};
export default reducer;