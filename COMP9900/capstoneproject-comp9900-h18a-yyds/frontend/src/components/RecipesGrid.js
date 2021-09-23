import React, { useState, useEffect, useRef } from "react";
import { makeStyles } from "@material-ui/core/styles";
import RecipeCard from "./RecipeCard";
import Card from "@material-ui/core/Card";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import AddRoundedIcon from "@material-ui/icons/AddRounded";
import { Container } from "@material-ui/core";
import { useHistory } from "react-router-dom";
import { Loader } from "./Loader";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    margin: "auto",
    width: "80%",
    "& > i": {
      margin: theme.spacing(8),
    },
  },
  uploadCard: {
    width: "inherit",
    minWidth: "225px",
    borderRadius: "1rem",
    padding: theme.spacing(2),
    boxSizing: "border-box",
    margin: "auto",
    textAlign: "center",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-around",
    alignItems: "center",
    borderStyle: "dashed",
  },
  gridContainer: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  gridCard: {
    width: "225px",
    padding: theme.spacing(4, 0),
  },
  uploadButton: {
    margin: theme.spacing(1.5, 0),
  },

  bottomOperations: {
    marginBottom: theme.spacing(4),
    textAlign: "center",
  },
}));

/**
 * Display all recipes from current user in profile page
 */
export default function RecipesGrid(props) {
  const history = useHistory();
  const {
    recipes,
    editable = false,
    handleDelete = null,
    setPage,
    totalNumber,
    isLoading,
  } = props;
  const classes = useStyles();
  const [pageNumber, setPageNumber] = useState(0);
  const [loading, setLoading] = useState(!isLoading);
  const bottomRef = useRef(null);

  const createRecipe = () => history.push("../postRecipe");

  const handleLoadMore = (pageCount) => {
    setPageNumber(pageCount + 1);
    setPage(pageCount + 1);
    setLoading(true);
  };

  useEffect(() => {
    if (pageNumber > 0) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [pageNumber, recipes]);

  useEffect(() => {
    if (recipes.length && loading) setLoading(false);
  }, [recipes]);

  return (
    <Container>
      <div className={classes.gridContainer}>
        <Grid container spacing={0}>
          {editable ? (
            <Grid
              container
              item
              className={classes.gridCard}
              xs={12}
              sm={4}
              md={3}
              justify="center"
            >
              <Card className={classes.uploadCard} variant="outlined">
                <AddRoundedIcon color="primary" style={{ fontSize: 60 }} />
                <Typography variant="h6">Upload Your Recipe</Typography>
                <Typography variant="caption">
                  Share recipes. Get feedback, likes and be a part of a growing
                  community.
                </Typography>
                <Button
                  className={classes.uploadButton}
                  variant="outlined"
                  color="secondary"
                  onClick={createRecipe}
                >
                  Upload Recipe
                </Button>
              </Card>
            </Grid>
          ) : null}
          {recipes &&
            recipes.map((recipe, i) => (
              <Grid
                key={i}
                container
                item
                xs={12}
                sm={4}
                md={3}
                justify="center"
                className={classes.gridCard}
              >
                <RecipeCard
                  recipe={recipe}
                  editable={editable}
                  handleDelete={handleDelete}
                />
              </Grid>
            ))}
        </Grid>
        <Container className={classes.bottomOperations}>
          {recipes.length !== totalNumber ? (
            !loading ? (
              <Button
                variant="outlined"
                color="primary"
                onClick={() => handleLoadMore(pageNumber)}
              >
                Load More
              </Button>
            ) : (
              <Loader />
            )
          ) : (
            <Typography variant="button" color="textSecondary">
              No More Results
            </Typography>
          )}
        </Container>
      </div>
      <div ref={bottomRef}></div>
    </Container>
  );
}
