import React from "react";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Divider from "@material-ui/core/Divider";

const useStyles = makeStyles((theme) => ({
  root: {
    background: "#fff",
    marginTop: 'auto'
  },
  footer: {
    padding: theme.spacing(2, 0)
  }
}));

const Copyright = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Divider />
      <Typography className={classes.footer} variant="body2" color="textSecondary" align="center">
        {`Copyright © COMP9900 Project ${new Date().getFullYear()}.`}
      </Typography>
    </div>
  );
};

export default Copyright;
