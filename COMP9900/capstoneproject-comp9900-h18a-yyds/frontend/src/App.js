import React from "react";
import { ThemeProvider } from "@material-ui/styles";
import { theme } from "./assets/css/palette";
import { Provider } from "react-redux";
import store from "./store";
import Main from "./pages/main";
import { PersistGate } from "redux-persist/lib/integration/react";
import { persistor } from "./store";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <Main />
        </PersistGate>
      </Provider>
    </ThemeProvider>
  );
}

export default App;
