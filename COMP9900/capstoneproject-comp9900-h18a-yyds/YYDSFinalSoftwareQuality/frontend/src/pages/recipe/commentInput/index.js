import React, { useState } from "react";
import PropTypes from "prop-types";
import { Box, Button, Paper, TextField, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import Rating from "@material-ui/lab/Rating";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    padding: theme.spacing(2),
    paddingBottom: 0,
    flexDirection: "column",
    justifyContent: "space-between",
    alignItems: "center",
    "& > *": {
      marginBottom: theme.spacing(2)
    }
  },
  btn: {
    alignSelf: "flex-end",
    width: "100px"
  }
}));

/**
 * View of the comment form on a recipe, consisting a text comment and a rate.
 */
const CommentInput = ({
  text,
  setText,
  readOnlyRating,
  rating,
  setRating,
  onSubmit
}) => {
  const classes = useStyles();
  const [hover, setHover] = useState(-1);

  return (
    <Paper variant="outlined" className={classes.root}>
      <Box display="flex" flexDirection="column" alignItems="center">
        <Box pr={"1ch"}>
          <Typography component="span" variant="overline">
            {readOnlyRating
              ? "Your most resent rating on this recipe"
              : "Rate this recipe"}
          </Typography>
        </Box>
        <Box display="flex" alignItems="center">
          <Rating
            name="controled-rating"
            value={rating}
            size="large"
            readOnly={readOnlyRating}
            onChange={(event, newValue) => {
              setRating(newValue);
            }}
            onChangeActive={(event, newHover) => {
              setHover(newHover);
            }}
          />
          <Box ml={1} minWidth={"1ch"}>
            {hover === -1 ? null : hover}
          </Box>
        </Box>
      </Box>
      <TextField
        fullWidth
        multiline
        rows={3}
        placeholder="Leave a comment..."
        variant="outlined"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <Button
        className={classes.btn}
        variant="contained"
        color="primary"
        disabled={text.trim().length === 0}
        disableElevation
        onClick={onSubmit}
      >
        Submit
      </Button>
    </Paper>
  );
};

CommentInput.propTypes = {
  text: PropTypes.string,
  setText: PropTypes.func,
  readOnlyRating: PropTypes.bool,
  rating: PropTypes.number,
  setRating: PropTypes.func,
  onSubmit: PropTypes.func
};

export default CommentInput;
