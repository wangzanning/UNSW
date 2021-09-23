import React, { useState } from "react";
import { useDispatch, useSelector, shallowEqual } from "react-redux";
import { useHistory } from "react-router";
import { makeStyles } from "@material-ui/styles";
import { Box, IconButton, Typography } from "@material-ui/core";
import Rating from "@material-ui/lab/Rating";
import { red } from "@material-ui/core/colors";
import StarRounded from "@material-ui/icons/StarRounded";
import FavoriteRoundedIcon from "@material-ui/icons/FavoriteRounded";
import FavoriteBorderRoundedIcon from "@material-ui/icons/FavoriteBorderRounded";
import {
  getLikedRecipes,
  likeRecipeByID,
  dislikeRecipeByID
} from "../services/like";
import { saveLikeList } from "../pages/login/store/actionCreators";
import { useEffect } from "react";

const useStyles = makeStyles((theme) => ({
  like: {
    color: red[500]
  },
  rating: {
    paddingRight: theme.spacing(1)
  },
  ratingBox: {
    background: "rgba(255,255,255,0.2)",
    borderRadius: "1em",
    padding: "2px 4px",
    backdropFilter: "blur(5px)"
  },
  number: {
    textAlign: "start",
    minWidth: "5ex",
    color: "inherit"
  }
}));

/**
 * The like and rating component.
 * @param {object} recipe The recipe object that contains total likes, total rate and rate number
 * @param {boolean} likedByMe Whether of not the current user has liked the recipe.
 * @param {object} classes Material ui makeStyles classes.
 * @returns
 */
export default function LikesAndRating({
  recipe,
  likedByMe = false,
  iconSize = "default"
}) {
  const classes = useStyles();
  const [numLikes, setNumLikes] = useState(recipe.liked_num);
  const [filled, setFilled] = useState(likedByMe);
  const dispatch = useDispatch();
  const history = useHistory();
  const { token,likeList } = useSelector(
    (state) => ({
      token: state.login.get("token"),
      likeList: state.login.get("likeList")
    }),
    shallowEqual
  );
  const getStart = () => {
    return recipe.rate_by === 0
      ? 0
      : Math.floor(recipe.rate_sum / recipe.rate_by);
  };
  
  const handleLike = (e) => {
    e.stopPropagation();
    if (!token) history.push('/login');
    else {
      setNumLikes(filled ? numLikes - 1 : numLikes + 1);
      setNumLikes(filled ? numLikes - 1 : numLikes + 1);
      if (filled) {
        // cancel like
        dislikeRecipeByID(recipe._id, token).then((res) => {
          if (res.msg === "dislike success")
            getLikedRecipes(undefined, token).then((res) =>
              dispatch(saveLikeList(res))
            );
        });
      } else {
        // post like
        likeRecipeByID(recipe._id, token).then((res) => {
          if (res.msg === "like success")
            getLikedRecipes(undefined, token).then((res) =>
              dispatch(saveLikeList(res))
            );
        });
      }
      setFilled(!filled);
    }
  };

  useEffect(() => {
    if (likeList.likes_list) {
      const isLiked = likeList.likes_list
        .filter(json => json.recipe_id === recipe._id).length > 0;
      if (isLiked) setFilled(true);
    }
  }, []);
  
  return (
    <Box display="flex" alignItems="center" justifyContent="space-between">
      <Box display="flex" alignItems="center">
        <IconButton
          edge="start"
          aria-label="add to favorites"
          className={classes.like}
          disabled={recipe.isUnavail}
          onClick={handleLike}
        >
          {filled ? (
            <FavoriteRoundedIcon fontSize={iconSize} />
          ) : (
            <FavoriteBorderRoundedIcon fontSize={iconSize} />
          )}
        </IconButton>
        <Typography variant="caption" className={classes.number}>
          {numLikes > 999 ? "999+" : numLikes}
        </Typography>
      </Box>
      <Box
        p={1}
        display="flex"
        alignItems="center"
        className={classes.ratingBox}
      >
        <Rating
          className={classes.rating}
          name="read-only"
          readOnly
          value={getStart()}
          icon={<StarRounded fontSize={iconSize} />}
        />
        <Typography variant="caption" className={classes.number}>
          {recipe.rate_by > 999 ? "999+" : recipe.rate_by}
        </Typography>
      </Box>
    </Box>
  );
}
