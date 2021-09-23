import React, { useState } from "react";
import { makeStyles } from '@material-ui/core/styles';
import { Paper, Stepper, Step, StepLabel, StepContent, Typography, Button } from "@material-ui/core";
import { CardMedia } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  root: {
    width: '90%',
    margin: '0 auto'
  },
  button: {
    marginTop: theme.spacing(1),
    marginRight: theme.spacing(1)
  },
  actionsContainer: {
    marginBottom: theme.spacing(2)
  },
  resetContainer: {
    padding: theme.spacing(3)
  },
  media: {
    height: "500px"
  }
}));

const Methods = ({ methods }) => {
  const classes = useStyles();
  const [activeStep, setActiveStep] = useState(0);

  const handleNext = () => {
    setActiveStep(prevActiveStep => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep(prevActiveStep => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };


  return (
    <div className={classes.root}>
      <Stepper activeStep={activeStep} orientation="vertical">
        {methods.map((method, i) => (
          <Step key={i}>
            <StepLabel>{`Step ${i + 1}`}</StepLabel>
            <StepContent>
              <Typography>{method.method ? method.method[0].toUpperCase() + method.method.slice(1) : ""}</Typography>
              {method.thumbnail ?
                <CardMedia className={classes.media} image={method.thumbnail} />
                : null}
              <div className={classes.actionsContainer}>
                <div>
                  <Button
                    disabled={activeStep === 0}
                    onClick={handleBack}
                    className={classes.button}
                  >
                    Back
                  </Button>
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={handleNext}
                    className={classes.button}
                  >
                    {activeStep === methods.length - 1 ? 'Finish' : 'Next'}
                  </Button>
                </div>
              </div>
            </StepContent>
          </Step>
        ))}
      </Stepper>
      {activeStep === methods.length && (
        <Paper square elevation={0} className={classes.resetContainer}>
          <Typography>You have completed all steps, enjoy your meal!</Typography>
          <Button variant="outlined" color="primary" onClick={handleReset} className={classes.button}>
            Restart
          </Button>
        </Paper>
      )}
    </div>
  );
};

Methods.propTypes = {};

export default Methods;
