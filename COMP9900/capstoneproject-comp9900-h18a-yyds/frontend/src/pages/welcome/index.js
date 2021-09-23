import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import {
  Box,
  Button,
  Container,
  makeStyles,
  Typography,
  Divider
} from "@material-ui/core";
import ArrowForwardIosRounded from "@material-ui/icons/ArrowForwardIosRounded";
import { getHottestNRecipes } from "../../services/feed";
import Slider from "../../components/Slider";
import clsx from "clsx";
import Tilt from "react-tilt";
import introData from "./introData";

const useStyles = makeStyles((theme) => {
  let textShadow = "";
  for (let i = 0; i < 80; i++) {
    textShadow += `${i}px ${i}px 0 ${theme.palette.grey[300]},`;
  }
  textShadow = textShadow.slice(0, -1);

  return {
    root: {},
    titleBox: {
      marginBottom: theme.spacing(2)
    },
    title: {
      fontWeight: 700,
      letterSpacing: "0.01em",
      "&$animate": {
        position: "relative",
        color: "transparent",
        "-webkit-text-stroke": `1px ${theme.palette.secondary.light}`
      }
    },
    animate: {
      "&::before": {
        content: "attr(data-text)",
        position: "absolute",
        left: 0,
        width: 0,
        overflow: "hidden",
        height: "100%",
        color: theme.palette.secondary.main,
        "-webkit-text-stroke": 0,
        borderRight: "2px solid",
        animation: "$animate 12s ease-in infinite",
        textShadow: textShadow
      }
    },
    "@keyframes animate": {
      "0%,20%,100%": { width: 0 },
      "40%, 95%": { width: "100%" }
    },
    btn: {
      padding: "0 4px",
      borderRadius: 0,
      borderBottom: "2px solid transparent",
      fontSize: "20px",
      letterSpacing: "0.01em",
      "&:hover": {
        borderBottom: "2px solid"
      }
    },
    hr: {
      flex: 1,
      margin: "0 20px"
    },
    intro: {
      flexFlow: "row wrap"
    },
    tiltCard: {
      width: "170px",
      height: "220px",
      border: "2px solid",
      borderRadius: "15px",
      padding: "10px",
      marginBottom: theme.spacing(4),
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      transformStyle: "preserve-3d",
      "&.active": { borderColor: theme.palette.secondary.main },
      "&:hover": {
        boxShadow: "0 20px 27px rgba(0, 0, 0, 0.1)"
      },
      "& > *": { transform: "translateZ(50px)" },
      "& img": {
        width: "100%",
        height: "100%",
        objectFit: "cover",
        transition: "all 0.2s ease-in"
      },
      "& h3": {
        textTransform: "uppercase",
        fontWeight: "700"
      },
      "& span": {
        textAlign: "center"
      },
      "&:hover $imgBox": {
        borderColor: theme.palette.secondary.main
      }
    },
    imgBox: {
      border: "10px solid rgba(0,0,0,0.1)",
      width: "100px",
      height: "100px",
      borderRadius: "50%"
    }
  };
});

function TiltCard({ image, imageAlt, title, subtitle, classes }) {
  const [mouseEnter, setMouseEnter] = useState(false);
  const options = {
    max: 30,
    perspective: 1500,
    scale: 1.05
  };

  return (
    <Tilt
      className={clsx(classes.tiltCard, mouseEnter ? "active" : "")}
      onMouseEnter={() => setMouseEnter(true)}
      onMouseLeave={() => setMouseEnter(false)}
      {...options}
    >
      <Box className={classes.imgBox}>
        <img src={mouseEnter ? imageAlt : image} alt="" />
      </Box>
      <Typography component="h3" color={mouseEnter ? "primary" : "initial"}>
        {title}
      </Typography>
      <Typography component="span" variant="subtitle2">
        {subtitle}
      </Typography>
    </Tilt>
  );
}

export default function Welcome() {
  const classes = useStyles();
  const history = useHistory();
  const [recipes, setRecipes] = useState();
  useEffect(() => {
    getHottestNRecipes()
      .then((result) => {
        setRecipes(result);
      })
      .catch((err) => console.log(err.message));
  }, []);

  return (
    <Container className={classes.root}>
      <Box
        className={classes.storyBoard}
        display="flex"
        flexWrap="wrap"
        alignItems="center"
        minHeight="45vh"
        mt={4}
      >
        <Box flex="400px 1" textAlign="start">
          <div className={classes.titleBox}>
            <Typography
              component="h1"
              variant="h2"
              className={classes.title}
              gutterBottom
            >
              Welcome to <br />
              <Typography
                component="span"
                variant="h1"
                data-text="MyRecipe"
                className={clsx(classes.title, classes.animate)}
              >
                MyRecipe
              </Typography>
            </Typography>
            <Typography>
              Everyone can cooke, it&apos;s just easier if they know the recipe.
            </Typography>
          </div>
          <Button
            className={classes.btn}
            onClick={() => history.push("/login")}
            color="primary"
          >
            Get Started
            <ArrowForwardIosRounded />
          </Button>
        </Box>
        <Box height="400px" flex="400px 1">
          {recipes && (
            <Slider recipes={recipes} autoPlay={true} stack={false} />
          )}
        </Box>
      </Box>
      <Box display="flex" alignItems="center" my={4}>
        <Divider className={classes.hr} />
        <Typography variant="h5">Explore, Share and More</Typography>
        <Divider className={classes.hr} />
      </Box>
      <Box
        className={classes.intro}
        display="flex"
        justifyContent="space-between"
        alignItems="center"
      >
        {introData &&
          introData.map((item) => (
            <TiltCard
              key={item.title}
              image={item.image}
              imageAlt={item.imageAlt}
              title={item.title}
              subtitle={item.subtitle}
              classes={classes}
            />
          ))}
      </Box>
    </Container>
  );
}
