import React, { useState, useEffect } from 'react';
import UserInfo from './userInfo';
import RecipesGrid from '../../components/RecipesGrid';
import { useSelector, shallowEqual } from "react-redux";
import { getFollowersList, getFollowingList, getRecipesList, getUser } from '../../services/profile';
import { getRecipeById } from '../../services/recipe';
import { getLikedRecipes } from '../../services/like';
import { ThemeProvider } from '@material-ui/styles';
import { theme } from '../../assets/css/palette';
import { useParams } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import { TabPanel } from './tabPanel';
import SwipeableViews from 'react-swipeable-views';
import { deleteRecipeById } from '../../services/profile';
import MessageAlert from '../../components/MessageAlert';
import FollowingList from './followingList';
import { unavailRecipe } from '../../assets/data/recipes';
import { PAGE_SIZE } from '../../utils/constant';
import loading from '../../assets/img/loading.gif';

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`
  };
}

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1,
    margin: 0,
    overflowY: 'scroll',
    position: 'relative'
  },
  loaderContainer: {
    display: 'flex',
    justifyContent: 'center',
    padding: 50
  },
  loader: {
    width: "120px"
  }
}));

export default function Profile() {

  const { token, followings, likeList, me } = useSelector(state => ({
    token: state.login.get("token"),
    followings: state.login.get("followings"),
    likeList: state.login.get("likeList"),
    me: state.login.get("user")
  }), shallowEqual);
  const [user, setUser] = useState({});
  const [recipes, setRecipes] = useState([]);                       // Exact list of recipe data
  const [likedRecipes, setLikedRecipes] = useState([]);             // Exact list of liked recipe data
  const [recipesList, setRecipesList] = useState([]);               // List if own recipe IDs
  const [likedRecipesList, setLikedRecipesList] = useState([]);     // List of liked recipe IDs
  const [value, setValue] = useState(0);                            // Handle tabs
  const [followingList, setFollowingList] = useState([]);           // List of following users
  const [followerList, setFollowerList] = useState([]);             // List of followers
  const [recipePage, setRecipePage] = useState(0);                  // Number of recipes page
  const [likedPage, setLikedPage] = useState(0);                    // Number of liked recipe page
  const [message, setMessage] = useState();
  const [isLoadingTab, setIsLoadingTab] = useState(true);
  const [isLoadingPage, setIsLoadingPage] = useState(false);
  const userId = useParams().id;
  const isMine = userId === me._id ? true : false;
  const isFollowing = followings && followings.includes(userId);
  const classes = useStyles();

  /**
   * Delete recipe, funtion will be triggered in RecipeCard
   * @param {string} recipeId
   */
  const handleDelete = (recipeId) => {
    deleteRecipeById(recipeId, token).then(res => {
      // Replace deleted recipe to unavailble
      const replaced = recipes.map(recipe => {
        return recipe._id === recipeId ? unavailRecipe : recipe;
      });
      setRecipes(replaced);
      setMessage({
        content: res.msg
      });
    }).catch(err => console.log(err.response));
  };

  /**
   * Load recipes according to page number
   * @param {number} pageCount - number of page
   */
  const fetchRecipesByPage = (type, recipeIdList, pageCount) => {
    // Justify is fetching uploaded recipes or liked recipes
    const setMethod = type === 'recipes' ? setRecipes : setLikedRecipes;
    const prevRecipeData = type === 'recipes' ? recipes : likedRecipes;
    const begin = isMine && type === 'recipes' ? pageCount * PAGE_SIZE - 1 : pageCount * PAGE_SIZE,
      end = isMine && type === 'recipes' ? begin + PAGE_SIZE - 1 : begin + PAGE_SIZE,
      target = recipeIdList.slice(begin, end);
    // setIsLoading(true);
    if (pageCount === 0) setIsLoadingTab(true);
    setIsLoadingPage(true);
    Promise.all(target.map(recipeId =>
      getRecipeById(recipeId)
        .then(recipe => {
          return recipe;
        })
        .catch(() => {
          return unavailRecipe;
        })
    )).then(res => {
      const newFetchedRecipes = res.filter(recipe => recipe !== 404);
      if (pageCount === 0) setMethod(newFetchedRecipes);
      else setMethod([...prevRecipeData, ...newFetchedRecipes]);
      if (pageCount === 0) setIsLoadingTab(false);
      setIsLoadingPage(false);
    });
  };

  const fetchFirstPage = (recipeIdList) => {
    setIsLoadingTab(true);
    const end = isMine ? 7 : 8;
    const target = recipeIdList.slice(0, end);
    Promise.all(target.map(recipeId =>
      getRecipeById(recipeId)
        .then(recipe => {
          return recipe;
        })
        .catch(() => {
          return unavailRecipe;
        })
    )).then(res => {
      const newFetchedRecipes = res.filter(recipe => recipe !== 404);
      setRecipes(newFetchedRecipes);
      setIsLoadingTab(false);
    });
  };

  const getUsersList = (userList, setUsers) => {
    Promise.all(userList.map(userId => getUser(userId, token)))
      .then(res => setUsers(res));
  };

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  const handleChangeIndex = (index) => {
    setValue(index);
  };

  const Loader = () => {
    return (
      <div className={classes.loaderContainer}>
        <img src={loading} className={classes.loader} />
      </div>
    );
  };

  useEffect(() => fetchRecipesByPage('recipes', recipesList, recipePage), [recipePage]);
  useEffect(() => fetchRecipesByPage('liked', likedRecipesList, likedPage), [likedPage]);

  // Fetch all own recipes ID and liked reicpes ID
  useEffect(() => {
    setRecipesList([]);
    setRecipes([]);
    setLikedRecipesList([]);
    setLikedRecipes([]);
    getUser(userId, token).then(userJson => {
      setUser(userJson);
      getRecipesList(userId, token).then(res => {
        const tmpRecipeList = res.recipe_list.map(recipe => recipe.recipe_id);
        setRecipesList(tmpRecipeList);
        fetchFirstPage(tmpRecipeList);
      }).then(() => {
        if (isMine) { // No need to fetch like list and followings list
          const tmpLikeList = likeList.likes_list.map(recipe => recipe.recipe_id);
          setLikedRecipesList(tmpLikeList);
          fetchRecipesByPage('liked', tmpLikeList, 0);
          getUsersList(followings, setFollowingList);
        } else
          getLikedRecipes(userId, token).then(res => {
            const tmpLikeList = res.likes_list.map(recipe => recipe.recipe_id);
            setLikedRecipesList(tmpLikeList);
            fetchRecipesByPage('liked', tmpLikeList, 0);
            getFollowingList(userId, token).then(res =>
              getUsersList(res.followings, setFollowingList));
          });
      }).then(() => {
        getFollowersList(userId, token).then(res =>
          getUsersList(res.followers, setFollowerList));
      });
    });
  }, [userId, value]);
  return (
    <ThemeProvider theme={theme}>
      <UserInfo user={user} isMine={isMine} followStatus={isFollowing} />
      <div className={classes.root}>
        <AppBar position="sticky">
          <Tabs
            value={value}
            onChange={handleChange}
            aria-label="simple tabs example"
            centered >
            <Tab label={`My Recipes ${recipesList.length}`} {...a11yProps(0)} />
            <Tab label={`My Likes ${likedRecipesList.length}`} {...a11yProps(1)} />
            <Tab label={`Followings`} {...a11yProps(2)} />
            <Tab label={`Followers`} {...a11yProps(3)} />
          </Tabs>
        </AppBar>
        {message ? <MessageAlert message={message} /> : null}
        <SwipeableViews
          axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
          index={value}
          onChangeIndex={handleChangeIndex}
        >
          <TabPanel value={value} index={0} dir={theme.direction} >
            {isLoadingTab ?
              <Loader /> :
              <RecipesGrid
                recipes={recipes}
                editable={isMine}
                handleDelete={handleDelete}
                totalNumber={recipesList.length}
                setPage={setRecipePage}
                isLoading={isLoadingPage}
              />}
          </TabPanel>
          <TabPanel value={value} index={1} dir={theme.direction}>
            {isLoadingTab ?
              <Loader /> :
              <RecipesGrid
                recipes={likedRecipes}
                totalNumber={likedRecipesList.length}
                setPage={setLikedPage}
                isLoading={isLoadingPage}
              />}
          </TabPanel>
          <TabPanel value={value} index={2} dir={theme.direction}>
            {isLoadingTab ?
              <Loader /> :
              <FollowingList users={followingList} followings={followings} />}
          </TabPanel>
          <TabPanel value={value} index={3} dir={theme.direction}>
            {isLoadingTab ?
              <Loader /> :
              <FollowingList users={followerList} followings={followings} />}
          </TabPanel>
        </SwipeableViews>
      </div>
    </ThemeProvider>
  );
}
