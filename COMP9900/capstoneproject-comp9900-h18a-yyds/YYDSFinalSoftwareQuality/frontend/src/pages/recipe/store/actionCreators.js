import * as actionTypes from './constants';

const changeRecipeDetail = (res) => ({
    type: actionTypes.SET_RECIPE_DETIAL,
    data: res.data
});

export const saveRecipeDetails = (res) => {
    return changeRecipeDetail(res);
};