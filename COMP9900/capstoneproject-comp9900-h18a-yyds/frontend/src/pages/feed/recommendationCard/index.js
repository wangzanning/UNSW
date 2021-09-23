import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import Box from "@material-ui/core/Box";
import { red } from "@material-ui/core/colors";
import Rating from "@material-ui/lab/Rating";
import StarRounded from "@material-ui/icons/StarRounded";
import FavoriteRoundedIcon from "@material-ui/icons/FavoriteRounded";
import FavoriteBorderRoundedIcon from "@material-ui/icons/FavoriteBorderRounded";
import CardActionArea from "@material-ui/core/CardActionArea";
import { ThemeProvider } from "@material-ui/styles";
import { theme } from "../../../assets/css/palette";

const useStyles = makeStyles((theme) => ({
  root: {
    borderRadius: "1rem",
    margin: theme.spacing(1, "auto"),
    width: "800px",
    height: "220px",
    background: "#DA9D42" /* fallback for old browsers */,
    background:
      "-webkit-linear-gradient(-90deg, #B75318, #DA9D42, #FFE7C2)" /* Chrome 10-25, Safari 5.1-6 */,
    //background: "linear-gradient(-90deg, #FFE7C2, #DA9D42, #B75318)" /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */,
    transition: "all 0.2s ease-in",
    "&:hover": {
      boxShadow: "0 0 40px 1px rgba(0,0,0,0.2)",
      transform: "translate(-0.1em, -0.1em) scale(1.01)",
    },
  },
  actionArea: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    height: "100%",
  },
  details: {
    flex: 1,
    height: "100%",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    padding: theme.spacing(1),
  },
  content: {
    flex: "1 0 auto",
  },
  coverContainer: {
    flex: "300px 0 1",
    borderRadius: theme.spacing(1),
  },
  cover: {
    maxWidth: "100%",
    height: "210px",
    borderRadius: theme.spacing(1),
  },
  controls: {
    display: "flex",
    alignItems: "center",
    paddingLeft: theme.spacing(1),
    paddingBottom: theme.spacing(1),
  },
  playIcon: {
    height: 38,
    width: 38,
  },
  like: {
    color: red[500],
  },
}));

/**
 * The large card displayed as a slide show at the top of a user's personal feed page.
 * @param {object} recipe The recipe being rendered out, returned from the database as is.
 * @param {bool} likedByMe True if the recipe is liked by current logged-in user.
 */
export default function RecommendationCard({ recipe, likedByMe = false }) {
  const classes = useStyles();

  const [numLikes, setNumLikes] = useState(recipe.liked_num);
  const [filled, setFilled] = useState(likedByMe);
  const getStart = () => {
    return recipe.rate_by === 0
      ? 0
      : Math.floor(recipe.rate_sum / recipe.rate_by);
  };
  const handleLike = () => {
    setNumLikes(filled ? numLikes - 1 : numLikes + 1);
    setFilled(!filled);
  };

  return (
    <ThemeProvider theme={theme}>
      <Card className={classes.root} elevation={0}>
        <CardActionArea component="div" className={classes.actionArea}>
          <div className={classes.details}>
            <CardContent className={classes.content}>
              <Typography component="h4" variant="h4" gutterBottom>
                {recipe.title[0].toUpperCase() + recipe.title.slice(1)}
              </Typography>
              {recipe.abstract && (
                <Typography variant="subtitle2" color="textSecondary">
                  {recipe.abstract[0].toUpperCase() + recipe.abstract.slice(1)}
                </Typography>
              )}
            </CardContent>
            <Box
              display="flex"
              alignItems="center"
              justifyContent="space-between"
              px={2}
            >
              <Box display="flex" alignItems="center">
                <IconButton
                  edge="start"
                  aria-label="add to favorites"
                  className={classes.like}
                  onClick={handleLike}
                >
                  {filled ? (
                    <FavoriteRoundedIcon />
                  ) : (
                    <FavoriteBorderRoundedIcon />
                  )}
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
                  {recipe.rate_by > 999 ? "999+" : recipe.rate_by}
                </Typography>
              </Box>
            </Box>
          </div>
          <Box className={classes.coverContainer} m={1}>
            <CardMedia
              component="img"
              className={classes.cover}
              image={recipe.image}
              title={recipe.title[0].toUpperCase() + recipe.title.slice(1)}
            />
          </Box>
        </CardActionArea>
      </Card>
    </ThemeProvider>
  );
}
