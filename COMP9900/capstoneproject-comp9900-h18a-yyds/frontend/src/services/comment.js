import request from "./axios";

/**
 * Post a new comment on the recipe.
 * @param {string} recipeId Id of the recipe being commented on.
 * @param {object} payload The payload send to the endpoint.
 * @param {string} token User authentication token.
 * @returns {Promise}
 */
export function postNewComment(recipeId, payload, token) {
  return request( {
    url: `recipes/comment?id=${recipeId}`,
    method: "post",
    headers: {
      'Content-Type': 'application/json',
      'token': token
    },
    data: JSON.stringify(payload)
  });
}

export function postNewRating(recipeId, rate, token) {
  return request({
    url: `users/rates?id=${recipeId}&rate=${rate}`,
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
      'token': token
    }
  });
}
