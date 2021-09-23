import React, { useState } from "react";
import Button from "@material-ui/core/Button";
import { useHistory } from "react-router-dom";
import { Container } from "@material-ui/core";
import { makeStyles } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import Avatar from "@material-ui/core/Avatar";
import TextField from "@material-ui/core/TextField";
import { useRef } from "react";
import CookingURL from "../../assets/img/salad.png";
import { useEffect } from "react";
import {
  putUserForgetPassword,
  postUserForgetPassword,
} from "../../services/login";
import { showFailuerMessage } from "../../utils/popMessage";
import { loginRequest, getUserDataRequest } from "../../services/login";
import { getFollowingList } from "../../services/profile";
import { getLikedRecipes } from "../../services/like";
import {
  saveToken,
  saveUserDetail,
  saveFollowingList,
  saveLikeList,
} from "../login/store/actionCreators";
import { useDispatch } from "react-redux";
import MessageAlert from "../../components/MessageAlert";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  divstyle: {
    display: "flex",
    height: "100%",
    justifyContent: "space-around",
    alignItems: "center",
  },
  boxstyle: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  halfscreen: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    width: "50%",
    flexDirection: "column",
    marginBottom: "15%",
  },
  findpasswordbutton: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
}));

export default function Welcome() {
  const classes = useStyles();
  const history = useHistory();
  const emailRef = useRef();
  const passRef = useRef();
  const dispatch = useDispatch();
  const [message, setMessage] = useState();
  const [show, setShowButton] = useState(false);

  const checkEmail = () => {
    let emailValue = document.getElementById("loginEmail").value;
    if (emailValue === "") {
      document.getElementById("loginEmail").style.backgroundColor =
        "rgb(201,89,77)";
      return false;
    } else {
      document.getElementById("loginEmail").style.backgroundColor = "";
      return true;
    }
  };

  const checkPass = () => {
    let passwordValue = document.getElementById("newpassword").value;
    if (passwordValue === "") {
      document.getElementById("newpassword").style.backgroundColor =
        "rgb(201,89,77)";
      return false;
    } else {
      document.getElementById("newpassword").style.backgroundColor = "";
      return true;
    }
  };

  function checkConfirm() {
    let doubleCheckValue = document.getElementById("Confirmpassword").value;
    if ("" === doubleCheckValue) {
      document.getElementById("Confirmpassword").style.backgroundColor =
        "rgb(201,89,77)";
      return false;
    } else {
      document.getElementById("Confirmpassword").style.backgroundColor = "";
      return true;
    }
  }

  function submitfindpasswordrequest() {
    const emailObject = {};
    let email = document.getElementById("loginEmail").value;
    emailObject.email = email.trim();
    console.log(emailObject);

    putUserForgetPassword(emailObject).then((res) => {
      console.log(res);
      if (res.msg === "successful") {
        alert("successful");
      } else {
        showFailuerMessage(res.msg);
      }
    });
  }

  function submitfindpassword() {
    let email = document.getElementById("loginEmail").value;
    let newpassword = document.getElementById("newpassword").value;
    let test = window.location.href;
    let index = test.indexOf("token=") + 6;
    let token = test.slice(index, test.length);

    let UserInfor = {};
    UserInfor.email = email;
    UserInfor.password = newpassword;

    postUserForgetPassword(UserInfor, token).then((res) => {
      console.log(res);
      const data = {
        email: email,
        password: newpassword,
      };
      loginRequest(data)
        .then((resp) => {
          if (resp) {
            const token = resp.token;
            getFollowingList(undefined, token)
              .then((res) => dispatch(saveFollowingList(res)))
              .then(() =>
                getLikedRecipes(undefined, token).then((res) => {
                  dispatch(saveLikeList(res));
                })
              )
              .then(() =>
                getUserDataRequest(token).then((res) =>
                  dispatch(saveUserDetail(res))
                )
              )
              .then(() => dispatch(saveToken(resp)))
              .then(() => {
                history.push("./feed");
              });
          }
        })
        .catch((err) =>
          setMessage({ content: err.message, severity: "error" })
        );
    });
  }

  useEffect(() => {
    const url = window.location.href;
    console.log(url);
    if (url.indexOf("token=") === -1) {
      setShowButton(false);
    } else {
      setShowButton(true);
    }
  }, []);

  return (
    <Container className={classes.divstyle}>
      <div className={classes.halfscreen}>
        <Container component="main" maxWidth="xs">
          <div className={classes.paper}>
            <Avatar src={CookingURL} alt="Pic"></Avatar>
            <Typography component="h1" variant="h5">
              Forget Password!
            </Typography>
            <form className={classes.form} noValidate>
              <div>
                <TextField
                  ref={emailRef}
                  onInput={checkEmail}
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  id="loginEmail"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  autoFocus
                />
                <div id="Findbutton">
                  {!show ? (
                    <Button
                      onClick={submitfindpasswordrequest}
                      fullWidth
                      variant="contained"
                      color="primary"
                      className={classes.submitFindpassword}
                    >
                      Find Password
                    </Button>
                  ) : null}
                </div>
              </div>

              {show ? (
                <div id="inputnewpassword" className={classes.inputnewpassword}>
                  <TextField
                    ref={passRef}
                    onInput={checkPass}
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    name="newpassword"
                    label="New Password"
                    type="newpassword"
                    id="newpassword"
                    autoComplete="current-password"
                  />
                  <TextField
                    ref={passRef}
                    onChange={checkConfirm}
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    name="Confirmpassword"
                    label="Confirm Password"
                    type="Confirm Password"
                    id="Confirmpassword"
                    autoComplete="current-password"
                  />

                  <Button
                    onClick={submitfindpassword}
                    fullWidth
                    variant="contained"
                    color="primary"
                    className={classes.submit}
                  >
                    Submit
                  </Button>
                  {message ? <MessageAlert message={message} /> : null}
                </div>
              ) : null}
            </form>
          </div>
        </Container>
      </div>
    </Container>
  );
}
