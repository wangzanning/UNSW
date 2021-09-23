import React from "react";
import drink from "../assets/img/drink.gif";
import loading from "../assets/img/loading.gif";
import { makeStyles } from "@material-ui/styles";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles(() => ({
  root: {
    height: "100vh",
    width: "100%",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    background: "#fffdf0",
    position: "absolute",
    top: 0,
    left: 0,
    zIndex: 2000,
    "& img": {
      width: "120px"
    },
    "& p": {
      textTransform: "uppercase"
    }
  },
  loader: {
    width: "100px",
    height: "100px",
    margin: "-10px auto",
    "& img": {
      width: "100%",
    }
  }
}));

export default function LoadingPage () {
  const classes = useStyles();
  return (
    <div className={classes.root}>
      <img src={drink} alt="a spinning glass of water with ice cubes in it" />
      <Typography component="p" variant="caption">Thank you for your patience</Typography>
    </div>
  );
}

export function Loader () {
  const classes = useStyles();
  return (
    <div className={classes.loader}>
      <img src={loading} alt="a spinning piece of pizza" />
    </div>
  );
}

