import React from "react";
import PropTypes from "prop-types";
import { useHistory } from "react-router-dom";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Link from "@material-ui/core/Link";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import MessageAlert from "../../../components/MessageAlert";
import { Avatar } from "@material-ui/core";
import CookingURL from "../../../assets/img/salad.png";

const useStyles = makeStyles((theme) => ({
  form: {
    width: "100%", // Fix IE 11 issue.
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  avatar: {
    backgroundColor: theme.palette.secondary.main,
  },
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "400px",
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

const OutlinedInput = (props) => {
  const classes = useStyles();

  return (
    <TextField
      className={classes.input}
      variant="outlined"
      margin="normal"
      color="primary"
      required
      fullWidth
      {...props}
    />
  );
};

const Form = ({ emailRef, passRef, onSubmit, message }) => {
  const classes = useStyles();
  const history = useHistory();

  const FindpasswordButton = () => {
    history.push("./forgetword");
  };

  const showSignUpButton = () => {
    history.push("./signUp");
  };

  return (
    <div className={classes.paper}>
      <Avatar src={CookingURL} alt="Pic"></Avatar>
      <Typography component="h1" variant="h5">
        Welcome to <span className={classes.myfront}>My</span>
        <span className={classes.myRecipe}>Recipe</span>!
      </Typography>
      <form className={classes.form} noValidate>
        <OutlinedInput
          inputRef={emailRef}
          id="loginEmail"
          label="Email Address"
          name="email"
          autoComplete="email"
          autoFocus
        />
        <OutlinedInput
          inputRef={passRef}
          name="password"
          label="Password"
          type="password"
          id="loginPassword"
          autoComplete="current-password"
        />
        <div className={classes.findpassword}>
          <Link variant="body2" onClick={FindpasswordButton}>
            {"Forget? Find it now!"}
          </Link>
        </div>
        <Button
          onClick={onSubmit}
          fullWidth
          variant="contained"
          color="primary"
          className={classes.submit}
        >
          Login In
        </Button>
        <Link variant="body2" onClick={showSignUpButton} color="primary">
          {"Don't have an account? Sign Up Now!"}
        </Link>
      </form>
      {message && <MessageAlert message={message} />}
    </div>
  );
};

Form.propTypes = {
  emailRef: PropTypes.object,
  passRef: PropTypes.object,
  onSubmit: PropTypes.func,
  message: PropTypes.object,
  setMessage: PropTypes.func,
};

export default Form;
