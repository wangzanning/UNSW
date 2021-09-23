import React, { useState } from "react";
import defaultAvatar from "../assets/img/avatar-15.png";
import { useHistory } from "react-router-dom";
import { useDispatch, useSelector, shallowEqual } from "react-redux";
import { Avatar, Fab, Menu, MenuItem, ListItemIcon, ListItemText } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
import FaceRoundedIcon from '@material-ui/icons/FaceRounded';
import ExitToAppRoundedIcon from '@material-ui/icons/ExitToAppRounded';

const useStyles = makeStyles(theme => ({
  avatar: {
    width: "52px",
    height: "52px"
  },
  menu: {
    marginTop: "10px",
    border: `1px solid ${theme.palette.primary}`
  },
  btn: {
    padding: "2px"
  },
  icon: {
    minWidth: "30px"
  }
}));

export default function HeaderAvator() {
  const classes = useStyles();
  const history = useHistory();
  const dispatch = useDispatch();
  const [anchorEl, setAnchorEl] = useState(null);
  const { user, token } = useSelector(
    (state) => ({
      token: state.login.get("token"),
      user: state.login.get("user")
    }),
    shallowEqual
  );

  const handleLogout = () => {
    dispatch({ type: "USER_LOGOUT" });
    setAnchorEl(null);
    history.push("/welcome");
  };

  const handleViewProfile = () => {
    setAnchorEl(null);
    history.push(`/profile/${user._id}`);
  };

  return (
    <>
      {token ? (
        <>
        <Fab className={classes.btn} onClick={(e) => setAnchorEl(e.currentTarget)} aria-haspopup="true" >
          <Avatar className={classes.avatar} src={user.headshot || defaultAvatar} alt="Avatar" />
        </Fab>
        <Menu
          className={classes.menu}
          anchorEl={anchorEl}
          keepMounted
          open={Boolean(anchorEl)}
          onClose={() => setAnchorEl(null)}
          anchorOrigin={{vertical: 'bottom', horizontal: 'center'}}
          transformOrigin={{vertical: 'top', horizontal: 'center'}}
          getContentAnchorEl={null}
        >
          <MenuItem onClick={handleViewProfile} divider button color="primary">
            <ListItemIcon className={classes.icon}><FaceRoundedIcon fontSize="small" /></ListItemIcon>
            <ListItemText primary="Profile" />
          </MenuItem>
          <MenuItem onClick={handleLogout} >
            <ListItemIcon className={classes.icon}><ExitToAppRoundedIcon fontSize="small" /></ListItemIcon>
            <ListItemText color="primary" primary="Logout" />
          </MenuItem>
        </Menu>
        </>
      ) : (
        <Fab className={classes.btn} onClick={() => history.push('/login')}>
          <Avatar className={classes.avatar} src={defaultAvatar} alt="Avatar"/>
        </Fab>
      )}
    </>
  );
}
