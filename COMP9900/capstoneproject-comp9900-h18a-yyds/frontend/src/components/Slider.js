import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { useSelector, shallowEqual } from "react-redux";
import { makeStyles } from "@material-ui/styles";
import ArrowForwardIosRoundedIcon from "@material-ui/icons/ArrowForwardIosRounded";
import ArrowBackIosRoundedIcon from "@material-ui/icons/ArrowBackIosRounded";
import clsx from "clsx";
import { IconButton, Typography } from "@material-ui/core";
import LikesAndRating from "./LikesAndRating";

const useStyles = makeStyles(() => ({
  root: {
    display: "flex",
    alignItems: "center",
    height: "100%",
    "& .btn-prev": {
      order: 1
    },
    "& .btn-next": {
      order: 3
    }
  },
  slider: {
    flex: 1,
    order: 2,
    height: "100%",
    perspective: "2000px",
    transformStyle: "preserve-3d",
    position: "relative"
  },
  card: {
    cursor: "pointer",
    opacity: 0,
    position: "absolute",
    width: (props) => (props.stack ? "70%" : "100%"),
    height: "100%",
    right: 0,
    left: 0,
    margin: "0 auto",
    borderRadius: "10px",
    overflow: "hidden",
    transition: props => props.stack
      ? "all 0.3s cubic-bezier(0.6, -0.38, 0.1, 1.28)"
      : "transform 0.3s cubic-bezier(0.03, 0.98, 0.52, 0.99), opacity 0.8s ease-in-out, box-shadow 0.8s ease-in-out",
    "&$active": {
      zIndex: 10,
      opacity: 1,
      boxShadow: "0 0px 30px 5px rgba(0,0,0,0.3)",
      transform: "translate3d(0,0,0)",
      "& $overlay": {
        opacity: 1
      }
    },
    "&$p2": {
      opacity: 1,
      boxShadow: "0 1px 4px 0 rgba(0,0,0,.37)",
      transform: "translate3d(-30%,0,-300px)",
      filter: "brightness(0.5)"
    },
    "&$p1": {
      opacity: 1,
      boxShadow: "0 6px 10px 0 rgba(0,0,0,.3), 0 2px 2px 0 rgba(0,0,0,.2)",
      transform: "translate3d(-18%,0,-200px)",
      filter: "brightness(0.7)"
    },
    "&$n1": {
      opacity: 1,
      boxShadow: "0 6px 10px 0 rgba(0,0,0,.3), 0 2px 2px 0 rgba(0,0,0,.2)",
      transform: "translate3d(18%,0,-200px)",
      filter: "brightness(0.7)"
    },
    "&$n2": {
      opacity: 1,
      boxShadow: "0 1px 4px 0 rgba(0,0,0,.37)",
      transform: "translate3d(30%,0,-300px)",
      filter: "brightness(0.5)"
    }
  },
  active: {},
  p1: {},
  p2: {},
  n1: {},
  n2: {},
  image: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    userSelect: "none",
    pointerEvents: "none"
  },
  overlay: {
    opacity: 0,
    color: "#eee",
    background: "rgba(0,0,0,0.5)",
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    boxShadow: "0px -40px 50px 20px rgb(0 0 0 / 50%)",
    padding: "0 50px 20px",
    transition: "inherit",
    "&:hover": {
      "& $subtitle": {
        opacity: 1,
        position: "relative"
      }
    }
  },
  title: {
    fontWeight: "700",
    color: "inherit"
  },
  subtitle: {
    position: "absolute",
    bottom: "-100%",
    color: "inherit",
    opacity: 0,
    transition: "all 0.2s ease"
  }
}));

const Arrow = ({ type, btnProps, iconProps }) => {
  return (
    <IconButton {...btnProps}>
      {type === "prev" ? (
        <ArrowBackIosRoundedIcon {...iconProps} />
      ) : (
        <ArrowForwardIosRoundedIcon {...iconProps} />
      )}
    </IconButton>
  );
};

const getNext = (index, total) => (index + 1) % total;
const getPrev = (index, total) => (index - 1 + total) % total;

export default function Slider({
  recipes,
  autoPlay = false,
  speed = 4000,
  orientation = "horizontal",
  showArrows = false,
  stack = true
}) {
  const classes = useStyles({ orientation, stack });
  const history = useHistory();
  const [current, setCurrent] = useState(0);
  const [p1, setP1] = useState();
  const [p2, setP2] = useState();
  const [n1, setN1] = useState();
  const [n2, setN2] = useState();
  const [paused, setPaused] = useState(autoPlay ? false : true);
  const { likeList } = useSelector(
    (state) => ({
      token: state.login.get("token"),
      likeList: state.login
        .get("likeList")
        ?.likes_list?.map((e) => e.recipe_id)
    }),
    shallowEqual
  );

  // Setting up slider auto-playing
  useEffect(() => {
    let timer;
    if (!paused) {
      timer = setInterval(() => {
        setCurrent((c) => getNext(c, recipes.length));
      }, speed);
    } else if (timer) {
      clearInterval(timer);
    }
    return () => clearInterval(timer);
  }, [paused, speed, recipes]);

  // Refresh the slider by updating current recipe, and as a result previous/next 2 recipes
  useEffect(() => {
    const prev = getPrev(current, recipes.length);
    const next = getNext(current, recipes.length);
    if (stack) {
      setP1(prev);
      setP2(getPrev(prev, recipes.length));
      setN1(next);
      setN2(getNext(next, recipes.length));
    }
  }, [current, recipes, stack]);

  // Map indices of recipes to class names so that they are dynamically styled
  const indexToClassName = (index) => {
    if (index === current) return clsx(classes.card, classes.active);
    else if (stack) {
      if (index === p1) return clsx(classes.card, classes.p1);
      if (index === p2) return clsx(classes.card, classes.p2);
      if (index === n1) return clsx(classes.card, classes.n1);
      if (index === n2) return clsx(classes.card, classes.n2);
    }
    return classes.card;
  };

  const handleClick = (recipe, index) => {
    index === current
      ? history.push(`recipe/${recipe._id}`)
      : setCurrent(index);
  };

  return (
    <div className={classes.root}>
      <div className={classes.slider}>
        {recipes.map((recipe, i) => (
          <div
            key={i}
            className={indexToClassName(i)}
            onClick={() => handleClick(recipe, i)}
            onMouseEnter={() => setPaused(true)}
            onMouseLeave={() => setPaused(autoPlay ? false : true)}
          >
            <img className={classes.image} src={recipe.image} alt="" />
            <div className={classes.overlay}>
              <Typography className={classes.title} variant="h4" gutterBottom>
                {recipe.title[0].toUpperCase() + recipe.title.slice(1)}
              </Typography>
              <Typography className={classes.subtitle}>
                {recipe.abstract
                  ? recipe.abstract[0].toUpperCase() + recipe.abstract.slice(1)
                  : ""}
              </Typography>
              <LikesAndRating
                recipe={recipe}
                likedByMe={likeList && likeList.includes(recipe._id)}
              />
            </div>
          </div>
        ))}
      </div>
      {showArrows && (
        <>
          <Arrow
            type="prev"
            btnProps={{
              className: "btn-prev",
              color: "primary",
              onClick: () => setCurrent((c) => getPrev(c, recipes.length))
            }}
            iconProps={{ fontSize: "large" }}
          />
          <Arrow
            type="next"
            btnProps={{
              className: "btn-next",
              color: "primary",
              onClick: () => setCurrent((c) => getNext(c, recipes.length))
            }}
            iconProps={{ fontSize: "large" }}
          />
        </>
      )}
    </div>
  );
}
