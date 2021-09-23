import request from "./axios";
import { getRecipeById } from "./recipe";

/**
 * Fetch the list of recipe ids that are published by all contributors that the
 * current user is subscribing to
 * @param {string} token
 * @returns Promise
 */
const getFeedIDs = (token) => {
  return request({
    url: "feeds/",
    method: "GET",
    headers: {
      token: token,
      "Content-Type": "application/json"
    }
  });
};

/**
 * Fetch feed list of recipes including recipe_id, liked_num and timestamp
 * @param {string} token
 * @returns Promise
 */
const getFeed = async (token) => {
  try {
    const res = await getFeedIDs(token);
    return res.msg;
  } catch (err) {
    console.log("get feed error", err.message);
  }
};

/**
 * A Helper function that's used to sort an array of recipes.
 * @todo Sort by number of likes current user for the contributor, and then full time
 * @param {object} a
 * @param {object} b
 * @returns {int}
 */
const byDateLikesThenTime = (a, b, numLikesForRecipeAuthors) => {
  const date1 = new Date(a.last_modified).setHours(0, 0, 0, 0);
  const date2 = new Date(b.last_modified).setHours(0, 0, 0, 0);
  const fullDate1 = new Date(a.last_modified);
  const fullDate2 = new Date(b.last_modified);
  return (
    date2 - date1 ||
    numLikesForRecipeAuthors[b.author_id] -
    numLikesForRecipeAuthors[a.author_id] ||
    fullDate2 - fullDate1
  );
};

/**
 * Fetch and return a sorted list of recipes.
 * @param {string} token
 * @returns
 */
export const getSortedFeed = async (token, likeList) => {
  let feed = await getFeed(token);
  const numLikesForRecipeAuthors = likeList.author_count.map((e) => {
    const n = {};
    n[e.author_id] = e.count;
    return n;
  });
  const feedList = feed.sort((a, b) =>
    byDateLikesThenTime(a, b, numLikesForRecipeAuthors)).map(recipe =>
      recipe.recipe_id);
  return feedList;
};

/**
 * Fetch recommended users for current user.
 * @param {string} token Auth token of current user.
 * @param {number} num Maximum number of recommended users returned, default to 10.
 * @returns {Promise} An array of user ids.
 */
export const getRecommendedUsers = async (token, num = 10) => {
  return await request({
    url: `feeds/users?n=${num}`,
    method: "GET",
    headers: {
      token: token,
      "Content-Type": "application/json"
    }
  });
};

export const getHottestNRecipes = async () => {
  try {
    const res = await request({
      url: 'feeds/hot',
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });
    return Promise.all(res.res.map(e => getRecipeById(e._id)));
  } catch (err) {
    console.error(err);
  }
};
