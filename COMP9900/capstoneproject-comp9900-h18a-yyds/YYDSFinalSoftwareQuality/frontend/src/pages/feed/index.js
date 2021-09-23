import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Typography, Container, Box, Button } from "@material-ui/core";
import ArrowUpwardRoundedIcon from "@material-ui/icons/ArrowUpwardRounded";
import Slider from "../../components/Slider";
import { getSortedFeed, getHottestNRecipes } from "../../services/feed";
import { shallowEqual, useSelector } from "react-redux";
import { getRecommendedUsers } from "../../services/feed";
import RecommendedUsers from "./recommendedUsers";
import RecipesGrid from "../../components/RecipesGrid";
import { getRecipeById } from "../../services/recipe";
import { PAGE_SIZE } from "../../utils/constant";
import LoadingPage from "../../components/Loader";

const useStyle = makeStyles((theme) => ({
  root: {
    marginTop: theme.spacing(2),
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-start",
  },
  gridContainer: {
    textAlign: "center",
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  gridCard: {
    width: "225px",
    padding: theme.spacing(4, 0),
  },
  avatarContainer: {
    display: "flex",
    height: "60px",
    flexDirection: "column",
    justifyContent: "space-between",
    alignItems: "center",
    padding: theme.spacing(0, 2),
    cursor: "pointer",
  },
  avatar: {
    transition: "all 0.1s ease-in",
    "&:hover": {
      background: theme.palette.secondary.light,
      boxShadow: "0 0 20px 0px rgba(0,0,0,0.1)",
      transform: "translate(-0.1em, -0.1em) scale(1.2)",
    },
  },
  myRecipe: {
    color: "black",
    fontSize: "40px",
  },
  boxstyle: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    marginTop: "30px",
    marginBottom: "0px",
  },
  scrollTopBtn: {
    opacity: props => props.showScrollBtn ? 1 : 0,
    position: "fixed",
    bottom: theme.spacing(7),
    right: theme.spacing(5)
  }
}));

/**
 * If a user is logged in, this is their personal feed page, apart from recipes
 * published by contributors that they are following, a recommondation section
 * is displayed based on their personal interest.
 */
export default function Feed() {
  const { token, likeList } = useSelector(
    (state) => ({
      token: state.login.get("token"),
      likeList: state.login.get("likeList"),
    }),
    shallowEqual
  );

  const [hotestNRecipes, setHotestNRecipes] = useState();
  const [recommendedUsers, setRecommendedUsers] = useState();
  const [page, setPage] = useState(0); // Page number of recipes
  const [feed, setFeed] = useState([]); // Array of recipe data
  const [feedList, setFeedList] = useState([]); // Array of feed recipe IDs
  const [ready, setReady] = useState(false);
  const [isLoadingPage, setIsLoadingPage] = useState(false);
  const [showScrollBtn, setShowScrollBtn] = useState(false);
  const classes = useStyle({ showScrollBtn });

  /**
   * Load recipes according to page number
   * @param {array} feedList - array of result recipes' ID
   * @param {number} pageCount - number of page
   */
  const fetchRecipesByPage = (feedList, pageCount) => {
    const begin = pageCount * PAGE_SIZE,
      end = begin + PAGE_SIZE,
      target = feedList.slice(begin, end);
    setIsLoadingPage(true);
    Promise.all(target.map((recipeId) => getRecipeById(recipeId))).then(
      (res) => {
        if (pageCount === 0) setFeed(res);
        else setFeed([...feed, ...res]); // append new into array of recipes
        setIsLoadingPage(false);
      }
    );
  };

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
    setShowScrollBtn(false);
  };

  useState(() => {
    getSortedFeed(token, likeList)
      .then((res) => {
        setFeedList(res);
        fetchRecipesByPage(res, 0);
      })
      .catch((err) => console.log(err.message));
    getHottestNRecipes()
      .then((res) => setHotestNRecipes(res))
      .catch((err) => console.log(err.message));
  }, []);

  useEffect(() => {
    getRecommendedUsers(token).then((res) => setRecommendedUsers(res.res));
  }, [token]);

  useEffect(() => {
    fetchRecipesByPage(feedList, page);
    page > 0 && setShowScrollBtn(true);
  }, [page]);

  useEffect(() => {
    hotestNRecipes && recommendedUsers && feed && setReady(true);
  }, [hotestNRecipes, recommendedUsers, feed]);

  if (!ready) return <LoadingPage />;
  return (
    <Container className={classes.root}>
      <Typography
        component="h1"
        variant="h5"
        gutterBottom
        className={classes.boxstyle}
      >
        <span className={classes.myRecipe}>
          Recipes and Contributors you might like
        </span>
      </Typography>
      {hotestNRecipes && (
        <Box height="400px" my={2}>
          <Slider
            recipes={hotestNRecipes}
            autoPlay={true}
            speed={4000}
            showArrows={true}
          />
        </Box>
      )}
      {recommendedUsers && (
        <RecommendedUsers users={recommendedUsers} classes={classes} />
      )}
      <Typography
        component="h1"
        variant="h5"
        gutterBottom
        className={classes.boxstyle}
      >
        <span className={classes.myRecipe}>Followings&apos; Sharings</span>
      </Typography>
      {feed && <div className={classes.gridContainer}>
        {!feed || feed.length === 0 ? (
          <Typography variant="button" color="textSecondary">
            Explore and follow more contributors to see more recipes.
          </Typography>
        ) : null}
        <RecipesGrid
          recipes={feed}
          totalNumber={feedList.length}
          setPage={setPage}
          isLoading={isLoadingPage}
        />
      </div>}
      <Button
        variant="outlined"
        color="primary"
        aria-label="back to top"
        onClick={scrollToTop}
        className={classes.scrollTopBtn}
      >
        <ArrowUpwardRoundedIcon />
      </Button>
    </Container>
  );
}
