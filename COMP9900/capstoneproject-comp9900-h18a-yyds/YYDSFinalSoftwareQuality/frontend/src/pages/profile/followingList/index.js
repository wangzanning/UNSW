import React from "react";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import { ThemeProvider } from "@material-ui/styles";
import { theme } from "../../../assets/css/palette";
import UserInfo from "../userInfo";


/**
 * Display list of user that the logged-in user is following
 *
 * @param {object} props
 */
export default function FollowingList(props) {
  const { users, followings } = props;
  return (
    <ThemeProvider theme={theme}>
      <List>
        {users.map(user =>
          <ListItem key={user._id}>
            <UserInfo user={user} followStatus={followings && followings.includes(user._id)} inList={true} />
          </ListItem>
        )}
      </List>
    </ThemeProvider>
  );
}
