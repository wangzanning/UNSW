import { createMuiTheme } from '@material-ui/core/styles';

/**
 * Define global color scheme
 */
export const theme = createMuiTheme({
  // Color scheme
  palette: {
    primary: {
      main: '#B75318'
    },
    secondary: {
      main: '#DA9D42'
    },
    textPrimary: {
      main: '#090B16'
    }, 
    textSecondary: {
      main: '#6E787F'
    },
    contrastThreshold: 3,
    tonalOffset: 0.2
  },

  // Font
  typography: {
    fontFamily: [
      'Poppins',
      '-apple-system',
      'Arial'
    ].join(',')
  }
});