import React from "react";
import { Container } from "@material-ui/core";
import { makeStyles } from "@material-ui/core";
import { useState, useEffect } from "react";
import { Typography } from "@material-ui/core";
import { IconButton } from "@material-ui/core";
import FavoriteRoundedIcon from "@material-ui/icons/FavoriteRounded";
import FavoriteBorderRoundedIcon from "@material-ui/icons/FavoriteBorderRounded";
import { red } from "@material-ui/core/colors";
import { Box } from "@material-ui/core";
import Rating from "@material-ui/lab/Rating";
import StarRounded from "@material-ui/icons/StarRounded";
import { Fab } from "@material-ui/core";
import Author from "../author";
import { likeRecipeByID, dislikeRecipeByID } from "../../../services/like";
import { getLikedRecipes } from "../../../services/like";
import { useDispatch } from "react-redux";
import { saveLikeList } from "../../../pages/login/store/actionCreators";
import { useSelector, shallowEqual } from "react-redux";

const useStyle = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    width: "90%",
    marginRight: "5%",
    marginLeft: "5%",
    marginTop: theme.spacing(2)
  },
  subroot: {
    display: "flex",
    justifyContent: "space-between",
    padding: "0px"
  },

  containersubroot: {
    padding: "0px"
  },
  media: {
    height: "100%"
  },
  paragrapy: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2)
  },
  likecontainer: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center"
  },
  like: {
    color: red[500]
  },
  rating: {
    paddingRight: theme.spacing(1)
  },
  number: {
    fontSize: "13px"
  },
  margin: {
    margin: theme.spacing(1)
  },
  extendedIcon: {
    marginRight: theme.spacing(1)
  },
  subroot2: {
    display: "flex",
    justifyContent: "flex-start",
    padding: "0px"
  },
  author: {
    margin: "0px"
  }
}));

export default function RecipeNameDetail(props) {
  const classes = useStyle();
  const dispatch = useDispatch();
  const { recipe, user } = props;
  const [numLikes, setNumLikes] = useState(0);
  const [rateby, setRatebBy] = useState(0);
  const [ratesum, setRateSum] = useState(0);
  const [filled, setFilled] = useState(false);

  const { token, likeList } = useSelector(
    (state) => ({
      token: state.login.get("token"),
      likeList: state.login.get("likeList")
    }),
    shallowEqual
  );

  useEffect(() => {
    setNumLikes(props.recipe.liked_num);
    setRatebBy(props.recipe.rate_by);
    setRateSum(props.recipe.rate_sum);
  }, []);

  useEffect(() => {
    if (likeList.likes_list) {
      const isLiked =
        likeList.likes_list.filter(
          (json) => json.recipe_id === props.recipe._id
        ).length > 0;
      if (isLiked) setFilled(true);
    }
  }, []);

  const getDate = () => {
    return new Date(recipe.last_modified).toLocaleString();
  };

  const handleLike = () => {
    if (filled) {
      // cancel like
      dislikeRecipeByID(props.recipe._id, token).then((res) => {
        if (res.msg === "dislike success")
          getLikedRecipes(undefined, token).then((res) => {
            dispatch(saveLikeList(res));
            setNumLikes(numLikes - 1);
          });
      });
    } else {
      // post like
      likeRecipeByID(props.recipe._id, token).then((res) => {
        if (res.msg === "like success")
          getLikedRecipes(undefined, token).then((res) => {
            dispatch(saveLikeList(res));
            setNumLikes(numLikes + 1);
          });
      });
    }
    setFilled(!filled);
  };

  const getStart = () => {
    return rateby === 0 ? 0 : Math.floor(ratesum / rateby);
  };

  return (
    <Container className={classes.root}>
      <Container className={classes.subroot2}>
        <Typography component="h1" variant="h4" className={classes.paragrapy}>
          {recipe.title[0].toUpperCase() + recipe.title.slice(1)}
        </Typography>
        <Box display="flex" alignItems="center">
          {recipe.meal_type ? ( //judge 是否为空
            recipe.meal_type instanceof Object ? ( // 判断
              recipe.meal_type.map((i) => (
                <Fab
                  variant="extended"
                  size="small"
                  color="primary"
                  aria-label="add"
                  className={classes.margin}
                  key={i}
                >
                  {i}
                </Fab>
              ))
            ) : (
              <Fab
                variant="extended"
                size="small"
                color="primary"
                aria-label="add"
                className={classes.margin}
              >
                {recipe.meal_type}
              </Fab>
            )
          ) : null}
        </Box>
      </Container>
      <Container className={classes.subroot}>
        {user ? <Author user={user} recipeId={props.recipe._id} /> : null}
        <Container className={classes.likecontainer}>
          <Box display="flex" alignItems="center">
            <IconButton
              edge="start"
              aria-label="add to favorites"
              className={classes.like}
              size="medium"
              onClick={handleLike}
            >
              {filled ? <FavoriteRoundedIcon /> : <FavoriteBorderRoundedIcon />}
            </IconButton>
            <Typography variant="caption" className={classes.number}>
              {numLikes > 999 ? "999+" : numLikes}
            </Typography>
          </Box>

          <Box display="flex" alignItems="center">
            <Rating
              className={classes.rating}
              name="read-only"
              readOnly
              value={getStart()}
              icon={<StarRounded />}
            />
            <Typography variant="caption" className={classes.number}>
              {rateby > 999 ? "999+" : rateby}
            </Typography>
          </Box>
        </Container>
      </Container>
      <Container className={classes.subroot}>
        <Container className={classes.containersubroot}>
          {recipe.abstract && (
            <Typography className={classes.paragrapy}>
              {recipe.abstract[0].toUpperCase() + recipe.abstract.slice(1)}
            </Typography>
          )}
        </Container>
      </Container>
      <Typography className={classes.paragrapy}>{getDate()}</Typography>
    </Container>
  );
}
