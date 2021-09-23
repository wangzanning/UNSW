import React from "react";
import {
  makeStyles,
  Box,
  Card,
  CardContent,
  Typography
} from "@material-ui/core";
import { StarRounded } from "@material-ui/icons";
import Rating from "@material-ui/lab/Rating";
import defaultRecipeImage from "../assets/img/salad.png";
import {theme} from '../assets/css/palette';
import { ThemeProvider } from '@material-ui/styles';


const useStyles = makeStyles(() => ({
  root: {
    cursor: "pointer",
    "&:hover": {
      borderRadius: "10px",
      "& $img": {
        borderRadius: "20px",
        width: "120px",
        height: "120px",
        top: "-20px",
        boxShadow: '0 20px 40px 1px rgba(0,0,20,0.1)'
      }
    },
    margin:'1px'
  },
  card: {
    position: "absolute",
    bottom: 0,
    left: 0,
    width: "100%",
    height: "120px",
    borderRadius: "20px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-end",
    background: "white" /* fallback for old browsers */,
    //background: "-webkit-linear-gradient(-90deg, #FFE7C2, #DA9D42,#B75318)" /* Chrome 10-25, Safari 5.1-6 */,
    border: '3px solid #B75318'


  },
  img: {
    position: 'absolute',
    zIndex: 1,
    top: 0,
    left: '50%',
    width: "110px",
    height: "110px",
    objectFit: "cover",
    borderRadius: "50%",
    background: "white",
    transform: "translateX(-50%)",
    transition: "all 0.25s cubic-bezier(0.68, -0.55, 0.27, 1.55)",
    border: '3px solid white',
    boxShadow: '0 -20px 40px 1px rgba(0,0,20,0.05), 0 20px 40px 1px rgba(255,255,255, 0.1)'
  },
  headerContent: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    marginTop:'0px'
  }
}));

const SmallRecipeCard = ({ recipe, onClick }) => {
  const classes = useStyles();
  const getStar = () => {
    return recipe.rate_by === 0
      ? 0
      : Math.floor(recipe.rate_sum / recipe.rate_by);
  };

  return (
    <ThemeProvider theme={theme}>
    <Box
      className={classes.root}
      position={"relative"}
      width={"160px"}
      height={"180px"}
      onClick={onClick}
    >
      <img
        className={classes.img}
        src={recipe.image === "string" || recipe.image.length === 0 ? defaultRecipeImage : recipe.image}
        alt="recipe cover"
        onError={(e)=>{e.target.onerror = null; e.target.src=defaultRecipeImage;}}
      />
      <Card className={classes.card} elevation={0}>
        <CardContent style={{ paddingBottom: "10px"}}>
          <Typography variant="caption" className={classes.headerContent} gutterBottom>
            {recipe.title[0].toUpperCase() + recipe.title.slice(1)}
          </Typography>
          <div>
            <Box display="flex" alignItems="center">
              <Rating
                className={classes.rating}
                name="rating"
                readOnly
                value={getStar()}
                icon={<StarRounded fontSize="small" />}
              />
              <Typography variant="caption" className={classes.headerContent}>
                {recipe.rate_by > 999 ? "999+" : recipe.rate_by}
              </Typography>
            </Box>
          </div>
        </CardContent>
      </Card>
    </Box>
    </ThemeProvider>

  );
};

export default SmallRecipeCard;
