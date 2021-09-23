import React from "react";
import { makeStyles } from "@material-ui/styles";
import pan from "../assets/img/pan.gif";
import pizza from "../assets/img/pizza.webp";

const useStyles = makeStyles(() => ({
  root: {
    position: "absolute",
    left: 0,
    width: "50vw",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: props => props.background,
    height: "inherit",
    '& img': {
      pointerEvents: "none",
      userSelect: "none"
    }
  }
}));

export const LoginAnimation = () => {
  const classes = useStyles({background: "#e7e0ce"});
  return (
    <div className={classes.root}>
      <img
        src={pan}
        alt="pan animation"
      ></img>
    </div>
  );
};

export const SignUpAnimation = () => {
  const classes = useStyles({background: "#d4f9f6"});
  return (
    <div className={classes.root}>
      <img
        src={pizza}
        alt="pizza animation"
      ></img>
    </div>
  );
};
