import request from "./axios";

/**
 * Fetch all recipes liked by current user
 * @param {string} userId
 */
export const getLikedRecipes = (userId = undefined, token) => {
  return request({
    url: userId ? `users/likes?id=${userId}` : `users/likes`,
    method: "GET",
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    }
  });
};

/**
 * Post like by recipe ID
 * @param {string} userId 
 * @param {string} token 
 */
export const likeRecipeByID = (recipeId, token) => {
  return request({
    url: `users/likes?id=${recipeId}`,
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'token': token
    }
  });
};

export const dislikeRecipeByID = (recipeId, token) => {
  return request({
    url: `users/likes?id=${recipeId}`,
    method: "DELETE",
    headers: {
      'Content-Type': 'application/json',
      'token': token
    }
  });
};
