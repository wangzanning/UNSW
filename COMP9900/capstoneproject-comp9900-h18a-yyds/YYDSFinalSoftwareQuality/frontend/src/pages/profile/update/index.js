import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Container from "@material-ui/core/Container";
import Button from "@material-ui/core/Button";
import Avatar from "@material-ui/core/Avatar";
import Box from "@material-ui/core/Box";
import Collapse from "@material-ui/core/Collapse";
import { useHistory } from "react-router-dom";
import { useSelector, shallowEqual } from "react-redux";
import { ThemeProvider } from "@material-ui/styles";
import { theme } from "../../../assets/css/palette";
import { updateUser, getUser } from "../../../services/profile";
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import CookingURL from '../../../assets/img/avatar-15.png';
import MessageAlert from '../../../components/MessageAlert';
import { useDispatch } from 'react-redux';
import { saveUserDetail } from "../../login/store/actionCreators";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    justifyContent: "center",
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4)
  },
  large: {
    width: theme.spacing(15),
    height: theme.spacing(15)
  },
  elements: {
    // border: '1px solid red',
    display: "flex",
    flexDirection: "column",
    width: "40%"
  },
  avatarElement: {
    padding: 0,
    display: "flex",
    justifyContent: "space-evenly",
    alignItems: "center",
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(4)
    // border: '2px solid green',
  },
  textElement: {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(4)
  },
  buttons: {
    padding: 0,
    display: "flex",
    justifyContent: "space-between"
  }
}));

/**
 * A profile management page that allows users to edit their own information.
 * Original information should be printed out in the input box and editable
 *
 * @param {object} props
 */
export default function Update() {
  const classes = useStyles();
  const history = useHistory();
  const dispatch = useDispatch();
  const { token, me } = useSelector(
    (state) => ({
      token: state.login.get("token"),
      me: state.login.get("user")
    }),
    shallowEqual
  );
  const [isUpdatingPassword, setIsUpdatingPassword] = useState(false);
  // Listen on user inputs
  const [avatar, setAvatar] = useState();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState();

  // Fetch user information
  useEffect(() => {
    setUsername(me.username);
    setEmail(me.email);
    setAvatar(me.headshot);
  }, []
  );

  /**
   * Create a local URL to display the image
   * actual file uploading will be handled in submit
   * @param {object} event
   */
  const handleChangeAvatar = (event) => {
    const reader = new FileReader();
    reader.readAsDataURL(event.target.files[0]);
    reader.onloadend = () => setAvatar(reader.result);
  };

  /**
   * Listen on the input of changing username
   * @param {*} event
   */
  const handleUsernameChange = (event) => setUsername(event.target.value);

  /**
   * Listen on the input of changing email
   * @param {*} event
   */
  const handleEmailChange = (event) => setEmail(event.target.value);

  /**
   * Listen on the input of typing old password
   * @param {*} event
   */
  const handleOldPassowrdChange = (event) => setOldPassword(event.target.value);

  /**
   * Listen on the input of typing new password
   * @param {*} event
   */
  const handleNewPassowrdChange = (event) => setNewPassword(event.target.value);

  const handleBackToProfile = () => history.push(`./profile/${me._id}`);

  /**
   * Only request for data which is updating
   * and them jump back to profile page
   */
  const handleSubmit = () => {
    const update = {};
    if (username.trim() !== me.username) update.username = username.trim();
    if (email.trim() !== me.email) update.email = email.trim();
    if (avatar !== me.headshot) {
      update.headshot = avatar;
    }
    // HANDLE RESET PASSWORD
    if (oldPassword.trim() && newPassword.trim()) {
      update.password = oldPassword.trim();
      update.newpassword = newPassword.trim();
    }
    if (Object.keys(update).length > 0) {
      updateUser(update, token).then(() =>
        getUser(undefined, token).then(user => {
          dispatch(saveUserDetail(user));
          setMessage({
            content: 'success',
            severity: 'success'
          });
        })).catch(err =>
          setMessage({
            content: err.response.status,
            severity: 'error'
          }));
    } else setMessage({
      content: 'You changed nothing.',
      severity: 'info'
    });
  };

  return (
    <ThemeProvider theme={theme}>
      <form onSubmit={handleSubmit} className={classes.root}>
        <Container className={classes.elements}>
          <Box display="flex">
            <Button
              color="primary"
              startIcon={<ArrowBackIcon />}
              onClick={handleBackToProfile}
            >
              Back to Profile
            </Button>
          </Box>
          <Container className={classes.avatarElement}>
            {avatar?
            <Avatar className={classes.large} src={avatar}></Avatar>
            :
            <Avatar className={classes.large} src={CookingURL}></Avatar>}
            <Container>
              <Button
                type="file"
                className={classes.button}
                variant="contained"
                color="primary"
                component="label"
              >
                Upload New Avatar
                <input
                  type="file"
                  accept="image/*"
                  hidden
                  onChange={handleChangeAvatar}
                />
              </Button>
            </Container>
          </Container>
          <TextField
            className={classes.textElement}
            label="Username"
            variant="outlined"
            value={username}
            onChange={handleUsernameChange}
          />
          <TextField
            className={classes.textElement}
            label="Email"
            variant="outlined"
            value={email}
            onChange={handleEmailChange}
          />

          <Collapse in={isUpdatingPassword}>
            <div style={{ display: "flex", flexDirection: "column" }}>
              <TextField
                className={classes.textElement}
                label="Old Password"
                variant="outlined"
                value={oldPassword}
                type="password"
                onChange={handleOldPassowrdChange}
              />
              <TextField
                className={classes.textElement}
                label="New Password"
                variant="outlined"
                value={newPassword}
                type="password"
                onChange={handleNewPassowrdChange}
              />
            </div>
          </Collapse>
          <Container className={classes.buttons}>
            <Button
              className={classes.textElement}
              onClick={() => setIsUpdatingPassword(!isUpdatingPassword)}
              variant="outlined"
              color="primary"
            >
              Update Password
            </Button>
            <Button
              type="submit"
              className={classes.textElement}
              variant="contained"
              color="primary"
            >
              Save Profile
            </Button>
          </Container>
          {message && <MessageAlert message={message} />}
        </Container>
      </form>
    </ThemeProvider>
  );
}
