import React from 'react';
import { Container } from '@material-ui/core';
import { makeStyles } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { Fab } from '@material-ui/core';
import { Box } from '@material-ui/core';
import 'antd/dist/antd.css';

const useStyle = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    width: '90%',
    marginRight: '5%',
    marginLeft: '5%',
    marginTop: theme.spacing(2)
  },

  subroot: {
    display: 'flex',
    flexWrap: 'wrap',
    flexDirection: 'row',
    padding: '0px'
  },
  subrootcolumn: {
    display: 'flex',
    flexWrap: 'wrap',
    flexDirection: 'column',
    padding: '0px'
  },
  media: {
    height: '100%'
  },
  paragrapy: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2)
  },
  avatarContaine: {
    display: "flex",
    height: "60px",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: theme.spacing(0, 2),
    cursor: "pointer"

  },
  avatar: {
    transition: "all 0.1s ease-in",
    '&:hover': {
      background: theme.palette.secondary.light,
      boxShadow: "0 0 20px 0px rgba(0,0,0,0.1)",
      transform: 'translate(-0.1em, -0.1em) scale(1.2)'
    },
    margin: '10px'
  },
  subrootrow: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'flex-start'

  },
  margin: {
    marginLeft: '10px'
  }
}));

export default function RecipeIngredient(props) {
  const classes = useStyle();
  const ingredients = props.ingredient;
  const halfLength = Math.floor(ingredients.length / 2);


  return (
    <Container className={classes.root}>
      <Typography component="h1" variant="h4" className={classes.paragrapy}>INGREDIENTS</Typography>

      <Container >
        <Container className={classes.subroot}>
          {ingredients.map(i => (
            <Box className={classes.avatarContainer} key={ingredients.i} >
              <Fab color="primary" variant="extended" size="small" className={classes.avatar} >
                {i.ingredient}
              </Fab>
            </Box>))
          }
        </Container >
        <Typography variant="h6" className={classes.paragrapy}>Ingredient Details</Typography>
      </Container >


      <Container className={classes.subrootrow}>
        <Container className={classes.subrootrow}>
          <Box >
            {ingredients.map(i => (
              ingredients.indexOf(i) <= halfLength ? (
                <Typography key={i.ingredient} >
                  {i.ingredient}</Typography>
              ) : null
            ))}
          </Box>
          <Box className={classes.margin}>
            {ingredients.map(i => (
              ingredients.indexOf(i) <= halfLength ?
                <Typography key={i.ingredient} id={i.ingredient}>
                  {i.volume} {i.unit}</Typography>
                : null
            ))}
          </Box>
        </Container>
        <Container className={classes.subrootrow}>
          <Box >
            {ingredients.map(i => (
              ingredients.indexOf(i) > halfLength ?
                <Typography key={i.ingredient} id={ingredients.indexOf(i)} >
                  {i.ingredient}</Typography>
                : null
            ))}
          </Box>
          <Box className={classes.margin}>
            {ingredients.map(i => (
              ingredients.indexOf(i) > halfLength ?
                <Typography key={i.ingredient}>{i.volume} {i.unit}</Typography>
                : null
            ))}
          </Box>
        </Container>
      </Container>
    </Container>


  );
}