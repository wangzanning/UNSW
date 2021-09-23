import request from "./axios";

/**
 * Search recipes by combination of recipe name, method, types and ingredients
 * Result should be a list of target recipe ids
 * @param {string} title 
 * @param {string} method 
 * @param {array} types 
 * @param {array} ingredients 
 * @returns 
 */
export const searchRequest = (title, method, types, ingredients) => {
  const titleQuery = title.replace(" ", "_");
  const methodQuery = method.replace(" ", "_");
  const typesQuery = types.map(type => type.replace(' ', '_')).join('+');
  const ingredientsQuery = ingredients.map(ingredient => ingredient.replace(' ', '_')).join('+');
  const queries = {
    'title': titleQuery,
    'methods': methodQuery,
    'meal_type': typesQuery,
    'ingredients': ingredientsQuery
  };
  let url = 'searches/?';
  Object.keys(queries).forEach(key => {
    if (queries[key]) url += `${key}=${queries[key]}&`;
  });
  url = url.substring(0, url.length - 1);
  return request({
    url: url,
    method: "GET",
    headers: {
      'Content-Type': 'application/json'
    }
  });
};
