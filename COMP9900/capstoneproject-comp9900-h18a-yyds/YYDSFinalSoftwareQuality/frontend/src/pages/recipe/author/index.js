import React from "react";
import { Avatar, Box, Button, Typography } from "@material-ui/core";
import { makeStyles } from '@material-ui/core';
import PersonIcon from '@material-ui/icons/Person';
import CookingURL from '../../../assets/img/avatar-15.png';
import { useState, useEffect } from 'react';
import { shallowEqual, useSelector, useDispatch } from "react-redux";
import { follow, unfollow } from '../../../services/profile';
import { getFollowingList } from '../../../services/profile';
import { saveFollowingList } from '../../login/store/actionCreators';
import { useHistory } from "react-router-dom";
import DoneRoundedIcon from '@material-ui/icons/DoneRounded';
import AddRoundedIcon from '@material-ui/icons/AddRounded';



const useStyle = makeStyles((theme) => ({
  root: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-start',
    width: '90%',
    margin: '0px'
  },
  gridContainer: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2)
  },
  avatarContainer: {
    display: "flex",
    height: "60px",
    flexDirection: "column",
    justifyContent: "space-between",
    alignItems: "center",
    padding: theme.spacing(0, 2),
    cursor: "pointer"
  },
  avatar: {
    transition: "all 0.1s ease-in",
    '&:hover': {
      background: theme.palette.secondary.light,
      boxShadow: "0 0 20px 0px rgba(0,0,0,0.1)",
      transform: 'translate(-0.1em, -0.1em) scale(1.2)'
    }
  },
  authorInfo: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    margin: '10px',
    width:'100px'
  }
}));

const Author = ({ user, recipeId }) => {
  const dispatch = useDispatch();
  const [isMine, setIsMine] = useState(false);
  const { me, followings, token } = useSelector(state => ({
    me: state.login.get("user"),
    followings: state.login.get("followings"),
    token: state.login.get("token")
  }), shallowEqual);
  const FollowingStatus = (followings && followings.includes(user._id)) ? true : false;
  const [isFollowing, setIsFollowing] = useState(FollowingStatus);
  const [followerNum, setFollowerNum] = useState(0);
  const history = useHistory();
  const classes = useStyle();

  useEffect(() => {
    setFollowerNum(user.follower_num);
    if (user._id === me._id) {
      setIsMine(true);
    }
  }, [user]);

  //follow or unfollow
  function handleFollowStatus() {
    if (isFollowing) unfollow(user._id, token)
      .then(() => {
        setFollowerNum(followerNum - 1);
        getFollowingList(undefined, token).then(res => dispatch(saveFollowingList(res)));
        setIsFollowing(false);
      });
    else follow(user._id, token)
      .then(() => {
        setFollowerNum(followerNum + 1);
        getFollowingList(undefined, token).then(res => dispatch(saveFollowingList(res)));
        setIsFollowing(true);
      });
  }
  function userProfile(){
    history.push(`/profile/${user._id}`);
  }

  return (
    <Box className={classes.root}>
      <Box className={classes.avatarContainer}>
        <Avatar className={classes.avatar}
          onClick={userProfile}
          alt={user.username}
          src={user.headshot ? user.headshot : CookingURL}>
          <PersonIcon fontSize="large" />
        </Avatar>
        <Typography component="span" variant="h6" color="textSecondary">
          {user.username ? user.username : "John"}</Typography>
      </Box>
      <Box className={classes.authorInfo}>
        <Typography>
          {`Recipes: ${user.recipe_num}`}
        </Typography>
        <Typography>
          {`Followers: ${followerNum}`}
        </Typography>
      </Box>
      <Box>
        {isMine ?
          <Button
            variant="outlined"
            color="primary"
            onClick={() => history.push(`/editRecipe/${recipeId}`)}
          >Edit
          </Button> :
          <Button
            variant="outlined"
            color="secondary"
            onClick={handleFollowStatus}
            startIcon={isFollowing ? <DoneRoundedIcon /> : <AddRoundedIcon />}>
            {isFollowing ? 'Following' : 'Follow'}
          </Button>
        }
        {/* {isUser ? null : (
          isFollowing ? (<Fab
            size="large"
            style={{ borderRadius: '0 1rem 0 1rem' }}
            aria-label="add"
            className={classes.margin}
            onClick={handleFollowStatus}
          >
            <DoneRoundedIcon />
            Unfollow
          </Fab>) : (<Fab
            size="small"
            color="primary"
            aria-label="add"
            className={classes.margin}
            onClick={handleFollowStatus}
            style={{ borderRadius: '0 1rem 0 1rem' }}
          >
            < AddRoundedIcon />
            follow
          </Fab>
          ))} */}
      </Box>
    </Box>
  );
};

Author.propTypes = {};

export default Author;
