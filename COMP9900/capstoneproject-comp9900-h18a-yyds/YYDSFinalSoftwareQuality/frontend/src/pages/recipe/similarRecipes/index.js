import React from "react";
import { Box, Typography } from "@material-ui/core";
import SmallRecipeCard from "../../../components/SmallRecipeCard";
import { useHistory } from "react-router";
import { theme } from '../../../assets/css/palette';
import { ThemeProvider } from '@material-ui/styles';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
  headerContent: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    marginTop: '0px'
  }
}));

const SimilarRecipes = ({ recipes }) => {
  const classes = useStyles();
  const history = useHistory();
  const handleClick = (e, recipe) => {
    history.push(`/recipe/${recipe._id}`);
  };
  return (
    <ThemeProvider theme={theme}>
      <Box width={'90%'} mb={5} marginX="auto" marginTop={'0px'} marginBottom={4}>
        <Typography variant="h5" className={classes.headerContent}>SIMILAR RECIPES </Typography>
        <Box display="flex" justifyContent="space-between" mt={4}>
          {recipes.map((recipe, i) => (
            <SmallRecipeCard key={recipe._id + i} recipe={recipe} onClick={(e) => handleClick(e, recipe)} />
          ))}
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default SimilarRecipes;
