import React, { useState } from 'react';
import PropTypes from "prop-types";
import Card from "@material-ui/core/Card";
import { makeStyles } from "@material-ui/core/styles";
import CardHeader from "@material-ui/core/CardHeader";
import CardMedia from "@material-ui/core/CardMedia";
import CardActionArea from "@material-ui/core/CardActionArea";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import { Button } from "@material-ui/core";
import { useHistory } from 'react-router';
import defaultRecipeImage from "../assets/img/salad2.png";
import LikesAndRating from './LikesAndRating';
import { unavailRecipe } from '../assets/data/recipes';

const useStyles = makeStyles((theme) => ({
  root: {
    width: "inherit",
    minWidth: "225px",
    borderRadius: "1rem"
  },
  header: {
    paddingTop: theme.spacing(1),
    paddingBottom: theme.spacing(1),
    textAlign: "start"
  },
  cardTitle: {
    display: "-webkit-box",
    "-webkit-box-orient": "vertical",
    "-webkit-line-clamp": 1,
    overflow: "hidden"
  },
  media: {
    height: 0,
    paddingTop: "56.25%" // 16:9
  },
  functionbuttonstyle: {
    display: 'flex'
  }
}));

/**
 * A basic recipe card view
 * @param {Object} recipe A recipe object being rendered, returned from backend and passed in as is
 * @param {Bool} likedByMe True if the recipe is liked by the logged-in user
 */
function RecipeCard({ recipe, likedByMe = false, editable = false, handleDelete = () => { } }) {
  const classes = useStyles();
  const history = useHistory();
  const [recipeData, setRecipeData] = useState(recipe);
  

  const getDate = () => {
    return new Date(recipeData.last_modified).toLocaleString();
  };

  const setUnavailable = () => {
    handleDelete(recipeData._id);
    setRecipeData(unavailRecipe);
  };

  const submitEdit = () => {
    history.push(`/editRecipe/${recipeData._id}`);
  };

  const jumpRecipeDetailed = () => {
    history.push(`/recipe/${recipeData._id}`);
  };

  return (
      <Card id={recipeData._id} className={classes.root} variant="outlined" >
        <CardActionArea disabled={recipeData.isUnavail} onClick={jumpRecipeDetailed}>
          <CardHeader
            className={classes.header}
            title={<Typography variant="h6" className={classes.cardTitle}>{recipeData.title[0].toUpperCase() + recipeData.title.slice(1)}</Typography>}
            subheader={<Typography variant="caption">{recipeData.isUnavail ? "Recipe has been deleted" : getDate()}</Typography>}
          />
          {recipeData.image==="string"||recipeData.image.length === 0 ?
            <CardMedia
              className={classes.media}
              image={defaultRecipeImage}
              title={recipeData.title}
            />:
            <CardMedia
            className={classes.media}
            image={recipeData.image}
            title={recipeData.title}
          />
          }
        </CardActionArea>
        <Box pl={2}>
          <LikesAndRating recipe={recipeData} likedByMe={likedByMe} iconSize="small" />
        </Box>
        {editable ?
          <Box display="flex">
            <Button
              onClick={submitEdit}
              fullWidth
              variant="outlined"
              color="primary"
              disabled={recipeData.isUnavail}
              className={classes.submitEdit}
              style={{ borderRadius: '0 0 0 1rem' }}
            >
              Edit
            </Button>
            <Button
              onClick={setUnavailable}
              disabled={recipeData.isUnavail}
              fullWidth
              variant="contained"
              color="primary"
              style={{ borderRadius: '0 0 1rem 0' }}
            >
              Delete
            </Button>
          </Box>
          : null}
      </Card>
  );
}

RecipeCard.propTypes = {
  recipe: PropTypes.object,
  likedByMe: PropTypes.bool,
  editable: PropTypes.bool
};

export default RecipeCard;
