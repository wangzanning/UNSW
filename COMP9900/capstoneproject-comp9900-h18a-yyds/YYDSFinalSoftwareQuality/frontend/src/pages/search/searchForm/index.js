import React from 'react';
import {
  TextField,
  Container,
  makeStyles,
  InputAdornment,
  Box,
  Button,
  Chip,
  Checkbox
} from '@material-ui/core';
import Autocomplete from '@material-ui/lab/Autocomplete';
import AssignmentRoundedIcon from '@material-ui/icons/AssignmentRounded';
import DynamicFeedRoundedIcon from '@material-ui/icons/DynamicFeedRounded';
import { theme } from '../../../assets/css/palette';
import { ThemeProvider } from '@material-ui/styles';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';

const useStyle = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(1),
    borderRadius: 6,
    backgroundColor: 'white',
    boxShadow: '10px 10px 5px #aaaaaa',
    position: 'relative',
    top: theme.spacing(10)
  },
  inputsGroup: {
    margin: theme.spacing(2, 0)
  },
  leftInput: {
    [`& fieldset`]: {
      borderRadius: `4px 0 0 4px`
    }
  },
  rightInput: {
    [`& fieldset`]: {
      borderRadius: `0 4px 4px 0`
    }
  },
  ingredientInput: {
    [`& fieldset`]: {
      borderRadius: 0
    }
  },
  formControl: {
    // width: '80%,'
    marginTop: theme.spacing(3)
  },
  chips: {
    display: 'flex',
    flexWrap: 'wrap'
  },
  chip: {
    margin: 2
  },
  outlinedInput: {
    "& legend": {
      visibility: "visible",
      color: 'grey'
    }
  },
  inputElements: {
    // margin: theme.spacing(3, 0)
    width: '50%'
  },
  submitButton: {
    borderRadius: `0 4px 4px 0`
  }
}));

export default function SearchForm(props) {
  const {
    query,
    handleRecipeNameChange,
    handleMethodChange,
    handleTypesChange,
    handleIngredientsChange,
    handleSubmit,
    allTypes
  } = props;
  const classes = useStyle();

  const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
  const checkedIcon = <CheckBoxIcon fontSize="small" />;

  return (
    <ThemeProvider theme={theme}>
      <div className={classes.root}>
        <Container>
          <Box display='flex' className={classes.inputsGroup}>
            <TextField
              className={classes.leftInput}
              fullWidth
              label="Recipe Name"
              variant="outlined"
              placeholder="Type name of recipe..."
              defaultValue={query.name || ""}
              onChange={event => handleRecipeNameChange(event.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <AssignmentRoundedIcon />
                  </InputAdornment>
                )
              }} />
            <TextField
              className={classes.rightInput}
              fullWidth
              label="Method"
              variant="outlined"
              placeholder="Type method..."
              defaultValue={query.method || ""}
              onChange={event => handleMethodChange(event.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <DynamicFeedRoundedIcon />
                  </InputAdornment>
                )
              }} />
          </Box>
          <Box display='flex' className={classes.inputsGroup}>
            <Autocomplete
              className={`${classes.inputElements} ${classes.leftInput}`}
              freeSolo
              limitTags={3}
              multiple
              options={allTypes}
              getOptionLabel={(option) => option}
              defaultValue={query.mealType || []}
              disableCloseOnSelect
              onChange={(event, value) => handleTypesChange(value)}
              renderOption={(option, { selected }) => (
                <React.Fragment>
                  <Checkbox
                    icon={icon}
                    checkedIcon={checkedIcon}
                    style={{ marginRight: 8 }}
                    checked={selected}
                  />
                  {option}
                </React.Fragment>
              )}
              renderInput={(params) => (
                <TextField
                  {...params}
                  variant="outlined"
                  label="Meal Type"
                  InputLabelProps={{ shrink: true }}
                  placeholder="Select meal types you want or type your own..."
                />
              )}
            />
            <Box className={classes.inputElements} display='flex'>
              <Autocomplete
                className={classes.ingredientInput}
                limitTags={4}
                fullWidth
                multiple
                freeSolo
                defaultValue={query.ingredients || []}
                options={[]}
                onChange={(event, value) => handleIngredientsChange(value)}
                renderTags={(value, getTagProps) =>
                  value.map((option, index) => (
                    <Chip variant="outlined" label={option} key="index" {...getTagProps({ index })} />
                  ))
                }
                renderInput={(params) => (
                  <TextField
                    {...params}
                    variant="outlined"
                    label="Ingredients"
                    InputLabelProps={{ shrink: true }}
                    placeholder="Type enter to add ingredients tags..."
                  />
                )}
              />
              <Button
                variant="contained"
                color="primary"
                type="submit"
                onClick={handleSubmit}
                className={classes.submitButton}
              >
                Search
              </Button>
            </Box>
          </Box>
        </Container>
      </div>
    </ThemeProvider >
  );
}
