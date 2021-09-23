import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Box from '@material-ui/core/Box';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`nav-tabpanel-${index}`}
      aria-labelledby={`nav-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          {children}
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired
};

function a11yProps(index) {
  return {
    id: `nav-tab-${index}`,
    'aria-controls': `nav-tabpanel-${index}`
  };
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper
  }
}));

export default function TabNav(props) { 
  // const children = props.children;
  const {children, isChange, setIsChange} = props;

  
  

  const classes = useStyles();
  const [value, setValue] = React.useState(0);
  const [description, ingredient, methods, comments] = [...children];

  const handleChange = (event, newValue) => {
    setValue(newValue);
    setIsChange(!isChange);
  };
  

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Tabs value={value} onChange={handleChange} aria-label="navigation tabs">
          <Tab label="Description" {...a11yProps(0)} />
          <Tab label="Ingredients" {...a11yProps(1)} />
          <Tab label="Method" {...a11yProps(2)} />
          <Tab label="Comments" {...a11yProps(3)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {description}
      </TabPanel>
      <TabPanel value={value} index={1}>
        {ingredient}
      </TabPanel>
      <TabPanel value={value} index={2}>
        {methods}
      </TabPanel>
      <TabPanel value={value} index={3}>
        {comments}
      </TabPanel>
    </div>
  );
}
