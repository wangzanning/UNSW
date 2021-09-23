import request from "./axios";

/**
 * Get user's token after login
 *
 * @param {string} data (id and password)
 * @returns user_token
 */
export function loginRequest(data) {
  return request( {
    url: "auth/login",
    method: "post",
    headers: {
      'Content-Type': 'application/json'
    },
    data: data
  });
}

/**
 * Get data of logged-in user
 *
 * @param {string} token
 */
export function getUserDataRequest(token) {
  return request( {
    url: "users",
    method: "get",
    headers: {
      'Content-Type': 'application/json',
      'token': token
    }
  });
}

/**
 * Get data of logged-in user
 *
 * @param {Object} personalEmail
 */
 export const putUserForgetPassword = (personalEmail)=> {
  return request({
    url: `/auth/reset`,
    method: "PUT", 
    headers: {
      'Content-Type': 'application/json'
    },
    data: personalEmail
  });
};

/**
 * Get data of logged-in user
 *
 * @param {Object} personalEmail
 */
 export const postUserForgetPassword = (personalInfor,token)=> {
  return request({
    url: `/auth/reset?token=${token}`,
    method: "POST", 
    headers: {
      'Content-Type': 'application/json'
    },
    data: personalInfor
  });
};