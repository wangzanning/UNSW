import request from "./axios";

/**
 * Make New Post
 *
 * @param {string} data (post detail)
 * @param {string} token (token)
 * @returns user_token
 */
export function getRecipeRequest(data,token) {
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
 * @returns all category
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

/**
 * edit recipe
 * * @param {object} data (edit detail)
 * @param {string} recipeId id
 * @param {string} token token
 * @returns {object} edit post detail
 */
export function editRecipeRequest(data, recipeId, token) {
  return request( {
    url: `recipes?id=${recipeId}`,
    method: "put",
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    },
    data: data
  });
}
