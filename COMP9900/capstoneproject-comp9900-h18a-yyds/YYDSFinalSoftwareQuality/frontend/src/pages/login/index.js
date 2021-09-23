import React, { memo, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { useRef } from 'react';
import { useDispatch } from 'react-redux';
import { useHistory } from "react-router-dom";
import { loginRequest, getUserDataRequest } from "../../services/login";
import { saveToken, saveUserDetail, saveFollowingList, saveLikeList } from "./store/actionCreators";
import { getFollowingList } from '../../services/profile';
import Form from './form';
import { getLikedRecipes } from '../../services/like';
import { LoginAnimation } from '../../components/AnimationFrames';

const useStyles = makeStyles((theme) => ({
  root: {
    position: "absolute",
    left: 0,
    right: 0,
    display: 'flex',
    height: '100%',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  formBox: {
    width: "50%",
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    [theme.breakpoints.up('lg')]: {
      justifyContent: 'start'
    }
  },
  imgBox: {
    width: "50%",
    height: "100%",
    position: "relative",
    zIndex: "-1"
  }
}));

export default memo(function LoginIn() { 
  const classes = useStyles();
  const emailRef = useRef();
  const passRef = useRef();
  const history = useHistory();
  const dispatch = useDispatch();
  const [message, setMessage] = useState();

  /**
   * Hanlde the submition of login form
   * @param {object} event
   */
  function submitLogin(event) {
    event.preventDefault();
    const data = {
      email: emailRef.current.value,
      password: passRef.current.value
    };
    // use new axios instead of fetch
    loginRequest(data).then(resp => {
      if (resp) {
        const token = resp.token;
        getFollowingList(undefined, token)
          .then(res => dispatch(saveFollowingList(res)))
          .then(() => getLikedRecipes(undefined, token)
            .then(res => { dispatch(saveLikeList(res)); }))
          .then(() => getUserDataRequest(token)
            .then(res => dispatch(saveUserDetail(res))))
          .then(() => dispatch(saveToken(resp)))
          .then(() => { history.push('./feed'); });
      }
    }).catch(err => setMessage({ content: err.message, severity: "error" }));
  }

  return (
    <Container className={classes.root}>
      <div className={classes.formBox}>
        <Form emailRef={emailRef} passRef={passRef} onSubmit={submitLogin} message={message} setMessage={setMessage} />
      </div>
      <div className={classes.imgBox}>
        <LoginAnimation />
      </div>
    </Container>
  );
 });
