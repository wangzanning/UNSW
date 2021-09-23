import * as actionTypes from './constants';

const changeTokenAction = (res) => ({
  type: actionTypes.SET_TOKEN,
  token: res.token
});

const changeUserDetail = (res) => ({
  type: actionTypes.SET_USER_DETAIL,
  user: res
});
const changeFollowingList = (res) => ({
  type: actionTypes.SAVE_FOLLOWING_LIST,
  followings: res.followings
});

const changeLikeList = (res) => ({
  type: actionTypes.SAVE_LIKE_LIST,
  likeList: res
});

//save token
export const saveToken = (res) => {
  return changeTokenAction(res);
};

export const saveFollowingList = (res) => {
  return changeFollowingList(res);
};
//save user detail
export const saveUserDetail = (res) => {
  return changeUserDetail(res);
};

export const saveLikeList = (res) => {
  return changeLikeList(res);
};