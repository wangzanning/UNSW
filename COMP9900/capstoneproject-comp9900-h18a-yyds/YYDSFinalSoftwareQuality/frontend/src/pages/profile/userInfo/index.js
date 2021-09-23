import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import Avatar from '@material-ui/core/Avatar';
import { useHistory } from "react-router-dom";
import { ThemeProvider } from '@material-ui/styles';
import { theme } from '../../../assets/css/palette';
import { follow, unfollow } from '../../../services/profile';
import { useSelector, shallowEqual, useDispatch } from "react-redux";
import { saveFollowingList } from '../../login/store/actionCreators';
import { getFollowingList } from '../../../services/profile';
import CookingURL from '../../../assets/img/avatar-15.png';
import DoneRoundedIcon from '@material-ui/icons/DoneRounded';
import AddRoundedIcon from '@material-ui/icons/AddRounded';
import { Divider } from '@material-ui/core';
import MessageAlert from '../../../components/MessageAlert';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    '& > *': {
      margin: theme.spacing(1)
    }
  },
  large: {
    width: theme.spacing(18),
    height: theme.spacing(18)
  },
  small: {
    width: theme.spacing(10),
    height: theme.spacing(10)
  },
  userContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '20px'
  },
  userInfoContainer: {
    width: '400px',
    margin: '0 80px'
  },
  email: {
    color: 'gray'
  },
  rowContainer: {
    margin: '10px 0',
    padding: 0,
    display: 'flex',
    justifyContent: 'space-between'
  },
  statistic: {
    padding: 0,
    margin: 0,
    textAlign: 'center'
  }
}));

export default function UserInfo(props) {
  const classes = useStyles();
  const history = useHistory();
  const dispatch = useDispatch();
  const { token, me } = useSelector(state => ({
    token: state.login.get("token"),
    me: state.login.get("user")
  }), shallowEqual);
  const { user, isMine = false, followStatus, inList = false } = props;
  const [isFollowing, setIsFollowing] = useState(followStatus);
  const [followerNum, setFollowerNum] = useState(0);
  const [message, setMessage] = useState();
  useEffect(() => setFollowerNum(user.follower_num), [user]);

  /**
   * Redirect user to edit page to update his/her info
   */
  const handleEdit = () => history.push(`/update`);

  /**
   * Enable user to subscribe/unsubscribe others
   * request sent depends on current following status.
   * Update stored following list
   */
  const handleFollowStatus = () => {
    // cannot follow myself
    if (user._id === me._id) {
      return setMessage({
        content: "You cannot follow yourself.",
        severity: "info"
      });
    }
    if (isFollowing)
      unfollow(user._id, token).then(res => {
        setFollowerNum(followerNum - 1);
        getFollowingList(undefined, token).then(res => dispatch(saveFollowingList(res)));
        setIsFollowing(false);
        setMessage({
          content: `Unfollowed ${res.msg}`
        });
      }).catch(err => setMessage({
        content: `Unfollowed ${err.msg}`
      }));
    else follow(user._id, token).then(res => {
      setFollowerNum(followerNum + 1);
      getFollowingList(undefined, token).then(res => dispatch(saveFollowingList(res)));
      setIsFollowing(true);
      setMessage({
        content: `Followed ${res.msg}`
      });
    }).catch(err => setMessage({
      content: `Unfollowed ${err.msg}`
    }));
  };

  return (
    <ThemeProvider theme={theme}>
      <Container className={classes.userContainer} theme={theme} >
        
        {user.headshot ?
          <Avatar
            className={inList ? classes.small : classes.large}
            src={user.headshot}
            onClick={() => history.push(`/profile/${user._id}`)} />
          : <Avatar
            className={inList ? classes.small : classes.large}
            src={CookingURL}
            onClick={() => history.push(`/profile/${user._id}`)} />}
        <Container className={classes.userInfoContainer}>
        {message && <MessageAlert message={message} />}
          <Container className={classes.rowContainer}>
            <Typography variant="h5">{user.username}</Typography>
            {isMine ?
              <Button variant="contained" color="primary" onClick={handleEdit}>Edit</Button> :
              <Button variant="outlined" color="secondary" onClick={handleFollowStatus}
                startIcon={isFollowing ? <DoneRoundedIcon /> : <AddRoundedIcon />}>
                {isFollowing ? 'Following' : 'Follow'}
              </Button>
            }
          </Container>

          <Container className={classes.rowContainer}>
            <Typography className={classes.email}>{user.email}</Typography>
          </Container>

          {inList ? null :
            <Container className={classes.rowContainer}>
              <Container className={classes.statistic}>
                <Typography variant="h6">{user.liked_num}</Typography>
                <Typography variant="overline">Likes</Typography>
              </Container>

              <Container className={classes.statistic}>
                <Typography variant="h6">{user.following_num}</Typography>
                <Typography variant="overline">Following</Typography>
              </Container>

              <Container className={classes.statistic}>
                <Typography variant="h6">{followerNum}</Typography>
                <Typography variant="overline">Followers</Typography>
              </Container>

            </Container>}
          {inList ? <Divider /> : null}

        </Container>

      </Container>
    </ThemeProvider>
  );
}
