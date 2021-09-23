import * as actionTypes from './constants';

const changeSearchQueries = searchQueries => ({
  type: actionTypes.SET_SEARCH_QUERIES,
  searchQueries: searchQueries
});

export const saveSearchQueries = (query) => {
  return changeSearchQueries(query);
};