import request from "./axios";

/**
 * Fetch a recipe by ID
 * @param {string} recipeId
 */
export const getRecipeById = (recipeId) => {
  return request({
    url: `recipes?id=${recipeId}`,
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  });
};

/**
 * Fetch the comments, paginated, on a given recipe.
 * @param {string} recipeId Id of the recipe
 * @param {number} pageNumber Number of the page, starting from 1
 * @returns {Promise}
 */
const fetchRecipeComments = (recipeId, pageNumber) => {
  return request({
    url: `recipes/comment?page=${pageNumber}&id=${recipeId}`,
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  });
};

/**
 * Returns an object containing a message and an array of comments on the given page.
 * @param {string} recipeId Id of the recipe
 * @param {number} pageNumber Number of the page, starting from 1
 * @returns {Promise}
 */
export const getRecipeComments = async (recipeId, pageNumber) => {
  try {
    return await fetchRecipeComments(recipeId, pageNumber);
  } catch (err) {
    console.log(err.message);
  }
};

const fetchRecommendationIds = (recipeId, num) => {
  return request({
    url: `recipes/recommend?n=${num}&id=${recipeId}`,
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  });
};

const fetchRecommendations = async (recipeIds) => {
  const recipes = await Promise.all(recipeIds.map(getRecipeById));
  return recipes;
};

/**
 * Returns an array of recipe Id's that are most similar to the given recipe.
 * @param {string} recipeId Id of the recipe.
 * @param {number} num Maximium number of similar recipes requested, default to 6.
 * @returns {Promise}
 */
export const getRecommendations = async (recipeId, num = 6) => {
  try {
    const res = await fetchRecommendationIds(recipeId, num);
    return await fetchRecommendations(res.res.map((e) => e._id));
  } catch (err) {
    console.log(err.message);
  }
};

/**
 * Fetch a user's rate for a recipe.
 * @param {string} recipeId The id of the recipe.
 * @param {string} token The auth token of the user.
 * @returns {Promise} The rate if the user has made one, null otherwise.
 */
export const getRate = async (recipeId, token) => {
  try {
    const response = await request({
      url: `users/rates?id=${recipeId}`,
      method: "GET",
      headers: {
        "token": token,
        "Content-Type": "application/json"
      }
    });
    return response.rate;
  } catch (err) {
    console.log(err.message);
  }
};
