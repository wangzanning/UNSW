import React from "react";
import { useHistory } from "react-router-dom";
import { Grid, Avatar, Typography } from "@material-ui/core";
import CookingURL from "../../../assets/img/avatar-15.png";

const RecommendedUsers = ({ users, classes }) => {
  const history = useHistory();

  return (
    <div className={classes.gridContainer}>
      <Grid container justify="center" spacing={0}>
        {users.map((user, i) => (
          <Grid key={i} item className={classes.avatarContainer}>
            <Avatar
              className={classes.avatar}
              alt="Avatar"
              src={user.headshot ? user.headshot : CookingURL}
              onClick={() => history.push(`/profile/${user._id}`)}
            >
              {user.username[0].toUpperCase()}
            </Avatar>
            <Typography
              component="span"
              variant="caption"
              color="textSecondary"
            >
              {user.username}
            </Typography>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default RecommendedUsers;
