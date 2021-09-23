import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import HeaderAvator from "./Avator";
import { useHistory } from "react-router-dom";
import { useSelector, shallowEqual } from "react-redux";
import SearchRoundedIcon from "@material-ui/icons/SearchRounded";
import PublishRoundedIcon from "@material-ui/icons/PublishRounded";

const useStyles = makeStyles((theme) => ({
  root: {
    position: "sticky",
    top: 0,
    background: props => props.transparent ? "transparent" : "#fff",
    boxShadow: props => props.transparent ? "unset": "0 10px 20px 0px rgba(0,0,0,0.05)",
    zIndex: 1000
  },
  toolbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: theme.spacing(1, 3)
  },
  title: {
    display: "none",
    [theme.breakpoints.up("sm")]: {
      display: "block"
    },
    "&:hover": {
      cursor: "pointer"
    }
  },
  search: {
    margin: "0 20px 0 auto"
  },
  upload: {
    marginRight: "20px"
  }
}));

export default function Header({ transparent=false }) {
  const classes = useStyles({ transparent });
  const history = useHistory();
  const { token } = useSelector(
    (state) => ({
      token: state.login.get("token")
    }),
    shallowEqual
  );

  return (
    <div className={classes.root}>
      <Toolbar className={classes.toolbar}>
        <Typography
          className={classes.title}
          noWrap
          onClick={() => history.push("/welcome")}
        >
          <Typography component="span" variant="h4" color="primary">My</Typography>
          <Typography component="span" variant="h5">Recipe</Typography>
        </Typography>
        <Button
          variant="outlined"
          color="primary"
          className={classes.search}
          startIcon={<SearchRoundedIcon />}
          onClick={() => history.push('/search')}
        >
          Search
        </Button>
        {token && (
          <Button
            variant="outlined"
            color="primary"
            className={classes.upload}
            startIcon={<PublishRoundedIcon />}
            onClick={() => history.push('/postRecipe')}
          >
            Upload
          </Button>
        )}
        <HeaderAvator />
      </Toolbar>
    </div>
  );
}
