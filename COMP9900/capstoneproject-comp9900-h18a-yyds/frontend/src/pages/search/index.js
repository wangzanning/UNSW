import React, { useState, useEffect } from "react";
import { ThemeProvider } from "@material-ui/styles";
import { theme } from "../../assets/css/palette";
import { Container, makeStyles, Typography, Button } from "@material-ui/core";
import ArrowUpwardRoundedIcon from "@material-ui/icons/ArrowUpwardRounded";
import { useDispatch, useSelector, shallowEqual } from "react-redux";
import { saveSearchQueries } from "./store/actionCreator";
import SearchForm from "./searchForm";
import RecipesGrid from "../../components/RecipesGrid";
import { getCategoryRequest } from "../../services/postRecipe";
import { searchRequest } from "../../services/search";
import backgroundImage from "../../assets/img/search-bg.jpg";
import { getRecipeById } from "../../services/recipe";
import MessageAlert from "../../components/MessageAlert";
import { PAGE_SIZE } from "../../utils/constant";

const useStyle = makeStyles((theme) => ({
  root: {},
  config: {
    backgroundImage: `url(${backgroundImage})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    marginBottom: theme.spacing(20)
  },
  searchTitle: {
    marginTop: theme.spacing(10),
    marginLeft: theme.spacing(8),
    fontWeight: 700,
    textShadow: "3px 5px 8px rgba(0,0,0,0.5)"
  },
  resultContainer: {
    marginTop: theme.spacing(20),
    display: "flex",
    justifyContent: "space-between"
  },
  searchResult: {
    border: "1px solid red",
    width: "50%"
  },
  notFound: {
    textAlign: "center",
    marginBottom: theme.spacing(10)
  },
  scrollTopBtn: {
    position: "fixed",
    bottom: theme.spacing(7),
    right: theme.spacing(5)
  }
}));

export default function Search() {
  const classes = useStyle();
  const dispatch = useDispatch();
  const { searchQueries } = useSelector(
    (state) => ({
      searchQueries: state.search.get("searchQueries")
    }),
    shallowEqual
  );
  const [allTypes, setAllTypes] = useState([]);
  const [recipeName, setRecipeName] = useState(searchQueries.name);
  const [method, setMethod] = useState(searchQueries.method);
  const [selectedTypes, setSelectedTypes] = useState(searchQueries.mealType); // array of all selected types
  const [ingredients, setIngredients] = useState(searchQueries.ingredients); // array of all typed ingredients
  const [results, setResults] = useState([]);
  const [recipeRes, setRecipeRes] = useState([]);
  const [page, setPage] = useState(0);
  const [isInitail, setIsInitial] = useState(false);
  const [message, setMessage] = useState();
  const [isLoadingPage, setIsLoadingPage] = useState(false);
  /**
   * Submit request to search in the combination of title, method, meal-type and ingredients
   * meal-type and ingredients are arrays of words
   * @param {object} event
   */
  const handleSubmit = () => {
    // Prompt to fill at least one
    if (
      recipeName === "" &&
      method === "" &&
      selectedTypes.length === 0 &&
      ingredients.length === 0
    )
      return setMessage({
        content: "Please fill out any fields to search.",
        severity: "warning"
      });
    setMessage(undefined);
    setIsInitial(false);
    // Initialization
    setResults([]);
    setRecipeRes([]);
    const query = {
      name: recipeName,
      method: method,
      mealType: selectedTypes,
      ingredients: ingredients
    };
    dispatch(saveSearchQueries(query));
    searchRequest(recipeName, method, selectedTypes, ingredients).then(
      (res) => {
        setResults(res.res); // save all result id in state
        if (res.res.length > 0) fetchRecipesByPage(res.res, 0); // display result in first page
      }
    );
  };

  /**
   * Load recipes according to page number
   * @param {array} resultsId - array of result recipes' ID
   * @param {number} pageCount - number of page
   */
  const fetchRecipesByPage = (resultsId, pageCount) => {
    const begin = pageCount * PAGE_SIZE,
      end = begin + PAGE_SIZE,
      target = resultsId.slice(begin, end);
    setIsLoadingPage(true);
    Promise.all(target.map((recipeId) => getRecipeById(recipeId._id))).then(
      (res) => {
        if (pageCount === 0) {
          // new search
          setPage(0);
          setRecipeRes(res);
        }
        // append new recipes into array of recipes results
        else setRecipeRes([...recipeRes, ...res]);
        setIsLoadingPage(false);
      }
    );
  };

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  useEffect(() => {
    getCategoryRequest().then((res) => {
      setAllTypes(res.types);
    });
    if (
      searchQueries.name === "" &&
      searchQueries.method === "" &&
      searchQueries.mealType.length === 0 &&
      searchQueries.ingredients.length === 0
    ) {
      setIsInitial(true);
    } else {
      handleSubmit();
    }
  }, []);

  useEffect(() => fetchRecipesByPage(results, page), [page]);

  return (
    <ThemeProvider theme={theme}>
      {message && <MessageAlert message={message} />}
      <div className={classes.config}>
        <Typography
          variant="h1"
          color="secondary"
          className={classes.searchTitle}
        >
          Find Recipes
          <br />
          You Like
        </Typography>
        <Container>
          <SearchForm
            className={classes.searchForm}
            query={searchQueries}
            handleRecipeNameChange={setRecipeName}
            handleMethodChange={setMethod}
            handleTypesChange={setSelectedTypes}
            handleIngredientsChange={setIngredients}
            handleSubmit={handleSubmit}
            allTypes={allTypes}
          />
        </Container>
      </div>
      {recipeRes.length > 0 ? (
        <div>
          <Container>
            <Typography variant="button" color="textSecondary">
              {`${results.length} recipes was found`}
            </Typography>
          </Container>
          <RecipesGrid
            recipes={recipeRes}
            setPage={setPage}
            totalNumber={results.length}
            isLoading={isLoadingPage}
          />
        </div>
      ) : (
        <Container className={classes.notFound}>
          <Typography variant="button" color="textSecondary">
            {isInitail
              ? "Search reicipes you want through configuration."
              : "No Recipes Found. Please try to search with other words."}
          </Typography>
        </Container>
      )}

      <Button
        variant="outlined"
        color="primary"
        aria-label="back to top"
        onClick={scrollToTop}
        className={classes.scrollTopBtn}
      >
        <ArrowUpwardRoundedIcon />
      </Button>
    </ThemeProvider>
  );
}
