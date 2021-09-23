import React from "react";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import {
  Avatar,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Typography
} from "@material-ui/core";
import Pagination from "@material-ui/lab/Pagination";
import { useHistory } from "react-router";
import defaultAvatar from "../../../assets/img/avatar-15.png";

const useStyle = makeStyles(() => ({
  pagination: {
    "& > ul": {
      justifyContent: "center"
    }
  }
}));

/**
 * The view a single comment on a recipe.
 * @param {object} comment A piece of comment data from the database.
 */
const Comment = ({ comment }) => {
  const history = useHistory();
  const getDate = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <ListItem alignItems="flex-start">
      <ListItemAvatar>
        <Avatar
          component="a"
          alt={comment.username}
          src={comment.avatar || defaultAvatar}
          onClick={() => history.push(`/profile/${comment.user_id}`)}
        >
          {comment.username[0].toUpperCase()}
        </Avatar>
      </ListItemAvatar>
      <ListItemText
        primary={comment.username}
        secondary={
          <>
            <Typography variant="caption">
              {getDate(comment.timestamp)}
            </Typography>
            <Typography variant="body1">{comment.content}</Typography>
          </>
        }
        secondaryTypographyProps={{ component: "div" }}
      />
    </ListItem>
  );
};

/**
 * The view of all comments on a recipe.
 * @param {array} comments An array consists a page of comments returned from the database.
 * @param {number} pageCount Total number of pages that the recipe has.
 * @param {number} currentPage Current page number of the comments.
 * @param {function} setCurrentPage A function that set the state commentPageNum.
 */
const Comments = ({ comments, pageCount, currentPage, setCurrentPage }) => {
  const classes = useStyle();
  const handleChange = (e, value) => {
    setCurrentPage(value);
  };

  return (
    <div>
      <List>
        {comments &&
          comments.map((comment, i) => (
            <React.Fragment key={comment._id}>
              <Comment comment={comment} />
              {i < comments.length - 1 && (
                <Divider variant="inset" component="li" />
              )}
            </React.Fragment>
          ))}
      </List>
      {comments.length === 0 ? (
        <Typography variant="body1" align="center" color="textSecondary" gutterBottom>No comment yet</Typography>
      ) : (
        <Pagination
          className={classes.pagination}
          count={pageCount}
          page={currentPage}
          variant="text"
          color="primary"
          onChange={handleChange}
        />
      )}
    </div>
  );
};

Comments.propTypes = {
  comments: PropTypes.array,
  pageNumber: PropTypes.number
};

export default Comments;
