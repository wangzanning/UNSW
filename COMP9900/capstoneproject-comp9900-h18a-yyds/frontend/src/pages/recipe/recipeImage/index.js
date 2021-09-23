import React from "react";
import { Container } from "@material-ui/core";
import { makeStyles } from "@material-ui/core";
import { CardMedia } from "@material-ui/core";
import defaultRecipeImage from "../../../assets/img/salad2.png";

const useStyle = makeStyles(() => ({
  root: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-start",
    height: "600px",
    padding: "0px"
  },
  media: {
    height: "100%"
  }
}));

export default function RecipeImage({ pic }) {
  const classes = useStyle();
  
  return (
    <Container className={classes.root}>
      <CardMedia className={classes.media} image={pic.length ===0 ||pic ==='string'? defaultRecipeImage: pic} />
    </Container>
  );
}
