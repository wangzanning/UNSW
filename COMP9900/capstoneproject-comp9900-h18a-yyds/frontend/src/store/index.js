import { createStore, compose, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import reducer from './reducer';
import { persistStore, persistReducer } from 'redux-persist';
import storageSession from 'redux-persist/lib/storage/session';
import immutableTransform from "redux-persist-transform-immutable";

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const storageConfig = {
  transforms: [
    immutableTransform()
  ],
  key: 'root',
  storage: storageSession,
  blacklist: [] // choose the data will not be persist
};
const myPersistReducer = persistReducer(storageConfig, reducer);

const store = createStore(myPersistReducer, composeEnhancers(
  applyMiddleware(thunk)
));

export const persistor = persistStore(store);
export default store;
