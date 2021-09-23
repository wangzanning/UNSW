import request from "./axios";

/**
 * Make New Post
 *
 * @param {string} data (post detail)
 * @param {string} token (token)
 * @returns user_token
 */
export function postRecipeRequest(data,token) {
  return request( {
    url: "recipes/",
    method: "post",
    headers: {
      'Content-Type': 'application/json',
      'token': token
    },
    data: data
  });
}

/**
 * Get all category
 *
 * @returns user_token
 */
export function getCategoryRequest() {
  return request( {
    url: "recipes/all",
    method: "get",
    headers: {
      'Content-Type': 'application/json'
    }
  });
}
