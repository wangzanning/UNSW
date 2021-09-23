import React, { memo, Suspense } from "react";
import { HashRouter } from "react-router-dom";
import { renderRoutes } from "react-router-config";
import routes from "../../router";
import Header from "../../components/Header";
import Copyright from "../../components/Copyright";
import { makeStyles } from "@material-ui/core/styles";
import { useSelector, shallowEqual } from "react-redux";
import LoadingPage from "../../components/Loader";

const useStyles = makeStyles(() => ({
  root: {
    height: "100%",
    display: "flex",
    flexDirection: "column"
  }
}));

export default memo(function Main() {
  const classes = useStyles();
  const { token } = useSelector(
    (state) => ({
      token: state.login.get("token")
    }),
    shallowEqual
  );

  return (
    <HashRouter>
      <div className={classes.root}>
        <Header transparent={!token}/>
        <Suspense fallback={<LoadingPage />}>
          {renderRoutes(routes, { isAuthenticated: !!token })}
        </Suspense>
        <Copyright />
      </div>
    </HashRouter>
  );
});
