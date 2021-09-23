import request from "./axios";

/**
 * Get user's token after signup
 *
 * @param {json} data (id and password)
 * @returns user_token
 */
export function signupRequest(data) {
  return request( {
    url: "auth/signup",
    method: "post",
    data: data,
    headers: {
      'Content-Type': 'application/json'
    }
  });
}

/**
 * Get user's token after login
 *
 * @param {string} token
 * @returns user_token
 */
export function newRecipeRequest(token) {
  return request( {
    url: "users/",
    method: "get",
    headers: {
      'Content-Type': 'application/json',
      'token': token
    }
  });
}
