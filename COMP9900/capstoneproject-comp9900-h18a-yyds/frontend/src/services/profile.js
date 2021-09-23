import request from "./axios";

/**
 * Get user's information to display profile page
 * 
 * @param {string} userId 
 * @returns 
 */
export const getUser = (userId, token) => {
  return request({
    url: userId ? `users/?id=${userId}` : 'users/',
    method: "GET",
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    }
  });
};

/**
 * Update user's personal information, only request updated values
 * 
 * @param {object} update - json of update fields
 * @returns 
 */
export const updateUser = (update, token) => {
  return request({
    url: `users`,
    method: "PUT",
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    },
    data: update
  });
};

/**
 * Get all recipes uploaded by user
 * @param {string} userId - ID of user to check
 * @param {string} token 
 * @returns fetch a list of recipeId uploaded by current user
 */
export const getRecipesList = (userId, token) => {
  return request({
    url: userId ? `users/recipes/?id=${userId}` : 'users/recipes',
    method: 'GET',
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    }
  });
};

/**
 * Get following list of current user
 * @param {string} userId 
 * @param {string} token 
 * @returns 
 */
export const getFollowingList = (userId, token) => {
  return request({
    url: userId ? `users/followings/?id=${userId}` : 'users/followings',
    method: 'GET',
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    }
  });
};

/**
 * Get follower list of current user
 * @param {string} userId 
 * @param {string} token 
 * @returns 
 */
export const getFollowersList = (userId, token) => {
  return request({
    url: userId ? `users/followers/?id=${userId}` : 'users/followers',
    method: 'GET',
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    }
  });
};

/**
 * Follow someone by ID
 * @param {string} userId 
 * @param {string} token 
 */
export const follow = (userId, token) => {
  return request({
    url: `users/followings/?id=${userId}`,
    method: "POST",
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    }
  });
};

/**
 * UNfollow someone by ID
 * @param {string} userId 
 * @param {string} token 
 */
 export const unfollow = (userId, token) => {
  return request({
    url: `users/followings/?id=${userId}`,
    method: "DELETE",
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    }
  });
};

/**
 * Delete recipe by ID
 * @param {string} recipesId 
 * @param {string} token 
 */
 export const deleteRecipeById = (recipesId, token) => {
  return request({
    url: `recipes/?id=${recipesId}`,
    method: "DELETE",
    headers: {
      'token': token,
      'Content-Type': 'application/json'
    }
  });
};
