import * as actionTypes from './constants';

const changeTokenAction = (res) => ({
  type: actionTypes.SET_TOKEN,
  token: res.token
});

export const saveToken = (res) => {
  return changeTokenAction(res);
};
