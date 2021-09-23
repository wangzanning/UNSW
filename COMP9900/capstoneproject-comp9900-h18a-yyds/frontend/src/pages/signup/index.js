import React from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Link from "@material-ui/core/Link";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import { useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { saveToken } from "../login/store/actionCreators";
import { signupRequest } from "../../services/signup";
import CookingURL from "../../assets/img/salad.png";
import MessageAlert from "../../components/MessageAlert";
import { getFollowingList } from "../../services/profile";
import {
  saveUserDetail,
  saveFollowingList,
  saveLikeList,
} from "../login/store/actionCreators";
import { getLikedRecipes } from "../../services/like";
import { getUserDataRequest } from "../../services/login";
import { SignUpAnimation } from "../../components/AnimationFrames";

const useStyles = makeStyles((theme) => ({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "400px",
  },
  avatar: {
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%",
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
    // background: '#B75318',
  },
  root: {
    position: "absolute",
    left: 0,
    right: 0,
    display: "flex",
    height: "100%",
    justifyContent: "space-between",
    alignItems: "center",
  },
  formBox: {
    width: "50%",
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    [theme.breakpoints.up("lg")]: {
      justifyContent: "start",
    },
  },
  imgBox: {
    width: "50%",
    height: "100%",
    position: "relative",
    zIndex: "-1",
  },
  textcolor: {
    color: "#B75318",
  },
  myfront: {
    color: "#B75318",
    fontSize: "40px",
  },
  myRecipe: {
    color: "black",
    fontSize: "26px",
  },
}));

export default function Signup() {
  const classes = useStyles();
  const [message, setMessage] = useState("");
  const doubleCheckPassRef = useRef();
  const emailRef = useRef();
  const nameRef = useRef();
  const passRef = useRef();
  const dispatch = useDispatch();
  const history = useHistory();

  function checkEmailSign() {
    let emailValue = document.getElementById("signupEmail").value;
    if (emailValue === "") {
      document.getElementById("signupEmail").style.backgroundColor =
        "rgb(201,89,77)";
      return false;
    } else {
      document.getElementById("signupEmail").style.backgroundColor = "";
      return true;
    }
  }

  //check name valid
  function checkNameSign() {
    let nameValue = document.getElementById("signupName").value;
    if (nameValue === "") {
      document.getElementById("signupName").style.backgroundColor =
        "rgb(201,89,77)";
      return false;
    } else {
      document.getElementById("signupName").style.backgroundColor = "";
      return true;
    }
  }

  //check password not empty
  function checkPassSign() {
    let passwordValue = document.getElementById("signupPassword").value;
    if (passwordValue === "") {
      document.getElementById("signupPassword").style.backgroundColor =
        "rgb(201,89,77)";
      return false;
    } else {
      document.getElementById("signupPassword").style.backgroundColor = "";
      return true;
    }
  }

  //check password same as last input
  function checkConfirm() {
    let passValue = document.getElementById("signupPassword").value;
    let doubleCheckValue = document.getElementById("signupDoublePassword")
      .value;
    if ("" === doubleCheckValue || passValue !== doubleCheckValue) {
      document.getElementById("signupDoublePassword").style.backgroundColor =
        "rgb(201,89,77)";
      return false;
    } else {
      document.getElementById("signupDoublePassword").style.backgroundColor =
        "";
      return true;
    }
  }

  function cancelSignUp() {
    history.push("./login");
  }

  //submit the sign message
  function submitSignButton(event) {
    event.preventDefault();
    let emailValue = document.getElementById("signupEmail").value;
    let passwordValue = document.getElementById("signupPassword").value;
    let nameValue = document.getElementById("signupName").value;
    const data = {
      email: emailValue,
      password: passwordValue,
      username: nameValue,
    };
    //check input before fetch
    if (!checkEmailSign() || !checkNameSign()) {
      setMessage({
        content: "Something is empty.",
        severity: "error",
      });
    } else if (!checkConfirm())
      setMessage({
        content: "Passwords are not same.",
        severity: "error",
      });
    else
      signupRequest(data)
        .then((resp) => {
          if (resp) {
            // save token here
            const token = resp.token;
            getFollowingList(undefined, token)
              .then((res) => dispatch(saveFollowingList(res)))
              .then(() =>
                getLikedRecipes(undefined, token).then((res) =>
                  dispatch(saveLikeList(res))
                )
              )
              .then(() =>
                getUserDataRequest(token).then((res) =>
                  dispatch(saveUserDetail(res))
                )
              )
              .then(() => dispatch(saveToken(resp)))
              .then(() => history.push("./feed"));
          }
        })
        .catch((err) => {
          if (err.response.status === 409) {
            setMessage({
              content: "Email has been registered",
              severity: "error",
            });
          }
        });
  }

  return (
    <Container className={classes.root}>
      <div className={classes.formBox}>
        <div className={classes.paper}>
          <Avatar src={CookingURL} alt="Pic"></Avatar>
          <Typography component="h1" variant="h5">
            Welcome to <span className={classes.myfront}>My</span>
            <span className={classes.myRecipe}>Recipe</span>!
          </Typography>
          <form className={classes.form} noValidate>
            <TextField
              ref={emailRef}
              onChange={checkEmailSign}
              variant="outlined"
              required
              fullWidth
              id="signupEmail"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
              margin="normal"
            />
            <TextField
              ref={nameRef}
              onChange={checkNameSign}
              autoComplete="fname"
              name="firstName"
              variant="outlined"
              required
              fullWidth
              id="signupName"
              label="User Name"
              margin="normal"
            />
            <TextField
              ref={passRef}
              onChange={checkPassSign}
              variant="outlined"
              required
              fullWidth
              id="signupPassword"
              label="Password"
              type="password"
              name="signupPassword"
              margin="normal"
            />
            <TextField
              ref={doubleCheckPassRef}
              onChange={checkConfirm}
              variant="outlined"
              required
              fullWidth
              name="password"
              label="Confirm Password"
              type="password"
              id="signupDoublePassword"
              margin="normal"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
              onClick={submitSignButton}
            >
              Sign Up
            </Button>
            <Link
              variant="body2"
              onClick={cancelSignUp}
              className={classes.textcolor}
            >
              Already have an account? Login in
            </Link>
          </form>
        </div>
        {message && <MessageAlert message={message} />}
      </div>
      <div className={classes.imgBox}>
        <SignUpAnimation />
      </div>
    </Container>
  );
}
