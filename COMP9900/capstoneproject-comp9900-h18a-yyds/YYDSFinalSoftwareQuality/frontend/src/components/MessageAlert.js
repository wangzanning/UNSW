import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Alert from "@material-ui/lab/Alert";
import Collapse from "@material-ui/core/Collapse";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
    "& > * + *": {
      marginTop: theme.spacing(2)
    }
  }
}));

/**
 * 
 * @param {object} message(object) The message being displayed, contains 2 fields:
 * - content string: the text content of the message
 * - severity string: one of `'success'`, `'warning'`, `'info'` or `'error'`, if not present, the alert's style defaults to `'success'`
 */
export default function ActionAlerts({message, ...rest}) {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  useEffect(() => {
    message && setOpen(true);
  }, [message]);

  return (
    <div className={classes.root}>
      <Collapse in={open}>
        <Alert
          severity={message.severity}
          {...rest}
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setOpen(false);
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
        >
          {message.content}
        </Alert>
      </Collapse>
    </div>
  );
}
