import React, { useState, useEffect } from "react";
import { useParams } from "react-router";
import RecipeImage from "./recipeImage";
import RecipeNameDetail from "./recipeNameDetail";
import RecipeIngredient from "./recipeIngredient";
import { Container, Paper, makeStyles } from "@material-ui/core";
import { shallowEqual, useSelector } from "react-redux";
import SimilarRecipes from "./similarRecipes";
import TabNav from "./tabNav";
import Methods from "./methods";
import Comments from "./comments";
import CommentInput from "./commentInput";
import { getUser } from "../../services/profile";
import {
  getRecipeComments,
  getRecommendations,
  getRecipeById,
} from "../../services/recipe";
import { postNewComment, postNewRating } from "../../services/comment";
import { getRate } from "../../services/recipe";
import LoadingPage from "../../components/Loader";

const useStyle = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-start",
  },
  paper: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  comments: {
    width: "90%",
    margin: "0 auto",
  },
}));

export default function Recipe() {
  const classes = useStyle();
  const { id } = useParams(); // recipe id
  const { token, user } = useSelector(
    (state) => ({
      token: state.login.get("token"),
      user: state.login.get("user"),
    }),
    shallowEqual
  );

  const [recipe, setRecipe] = useState();
  const [recipeAuthor, setRecipeAuthor] = useState();
  const [comments, setComments] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [newComment, setNewComment] = useState("");
  const [newRating, setNewRating] = useState(0);
  const [rated, setRated] = useState(false); // whether or not I have already rated the recipe
  const [rerender, setRerender] = useState(false); //used only to force a rerender
  const [similarRecipes, setSimilarRecipes] = useState();
  const [isChange, setIsChange] = useState(false);
  const [ready, setReady] = useState(false);

  // Load recipe details
  useEffect(() => {
    getRecipeById(id).then((res) => {
      setRecipe(res);
    });
  }, [id, isChange]);

  // Load author info as well as similar recipes
  useEffect(() => {
    if (recipe && token) {
      getUser(recipe.author_id, token)
        .then((res) => setRecipeAuthor(res))
        .catch((err) => console.log(err.message));

      getRate(recipe._id, token).then((res) => {
        if (res) {
          setNewRating(res);
          setRated(true);
        }
      });

      getRecommendations(recipe._id)
        .then(setSimilarRecipes)
        .catch((err) => console.log(err.message));
    }
  }, [recipe, token]);

  // Load a page of comments
  useEffect(() => {
    if (recipe) {
      const l = recipe.comments_pages.length;
      if (l === 0) {
        setComments([]);
      } else {
        getRecipeComments(recipe._id, l - currentPage + 1).then((res) => {
          try {
            setComments(res.comments.reverse());
          } catch (err) {
            setComments([]);
          }
        });
      }
    }
  }, [currentPage, recipe]);

  // Force rerendering the comment page, happens only when the user leaves a comment on page 1
  useEffect(() => {
    if (rerender) {
      const l = Math.max(recipe.comments_pages.length, 1);
      setRerender(false);
      getRecipeComments(recipe._id, l).then((res) => {
        setComments(res.comments.reverse());
      });
    }
  }, [rerender, recipe]);

  useEffect(() => {
    recipe && recipeAuthor && similarRecipes && setReady(true);
  }, [recipe, recipeAuthor, similarRecipes]);

  // Submit new comment (must be non-empty) and rate (optional, won't submit rate if 0)
  const submitComment = () => {
    if (newComment.trim()) {
      const commentPayload = {
        user_id: user._id,
        content: newComment.trim(),
        reply_to: "",
        timestamp: new Date().getTime(),
      };
      setNewComment("");
      postNewComment(recipe._id, commentPayload, token)
        .then(() => {
          setCurrentPage(1);
          currentPage === 1 && setRerender(true); // forces a rerender when setCurrentPage does not
        });
      !rated &&
        newRating &&
        postNewRating(recipe._id, newRating, token).then(() => {
          setRated(true);
        });
    }
  };

  const update = (value) => {
    setIsChange(value);
  };

  return (
    <Container className={classes.root}>
      {ready ? (
        <Paper className={classes.paper} elevation={3}>
          <RecipeImage pic={recipe.image} />
          <TabNav isChange={isChange} setIsChange={update}>
            <RecipeNameDetail recipe={recipe} user={recipeAuthor} />
            <RecipeIngredient ingredient={recipe.ingredients} />
            <Methods methods={recipe.methods} />
            <Container className={classes.comments}>
              <CommentInput
                text={newComment}
                setText={setNewComment}
                readOnlyRating={rated}
                rating={newRating}
                setRating={setNewRating}
                onSubmit={submitComment}
              />
              <Comments
                comments={comments}
                pageCount={recipe.comments_pages.length}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
              />
            </Container>
          </TabNav>
          {similarRecipes && <SimilarRecipes recipes={similarRecipes} />}
        </Paper>
      ) : (
        <LoadingPage />
      )}
    </Container>
  );
}
