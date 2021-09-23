import React from "react";
import { Redirect } from "react-router-dom";

const Login = React.lazy(() => import("../pages/login"));
const Signup = React.lazy(() => import("../pages/signup"));
const Welcome = React.lazy(() => import("../pages/welcome"));
const Profile = React.lazy(() => import("../pages/profile"));
const Feed = React.lazy(() => import("../pages/feed"));
const PostRecipe = React.lazy(() => import("../pages/postRecipe"));
const UpdateProfile = React.lazy(() => import("../pages/profile/update"));
const ForgetPassword = React.lazy(() => import("../pages/password"));
const Recipe = React.lazy(() => import('../pages/recipe'));
const Search = React.lazy(() => import('../pages/search'));
const EditRecipe = React.lazy(() => import('../pages/editRecipe'));

const routes = [
  {
    path: "/",
    exact: true,
    render: ({ isAuthenticated }) => isAuthenticated ? <Redirect to='/feed' /> : <Redirect to="/welcome" />
  },
  {
    path: "/welcome",
    render: ({ isAuthenticated }) => isAuthenticated ? <Redirect to='/feed' /> : <Welcome />
  },
  {
    path: "/login",
    render: ({ isAuthenticated }) => isAuthenticated ? <Redirect to='/feed' /> : <Login />
  },
  {
    path: "/signup",
    render: ({ isAuthenticated }) => isAuthenticated ? <Redirect to='/feed' /> : <Signup />
  },
  {
    path: "/profile/:id",
    render: ({ isAuthenticated }) => isAuthenticated ? <Profile /> : <Redirect to='/login' />
  },
  {
    path: "/update",
    render: ({ isAuthenticated }) => isAuthenticated ? <UpdateProfile /> : <Redirect to='/login' />
  },
  {
    path: "/postRecipe",
    render: ({ isAuthenticated }) => isAuthenticated ? <PostRecipe /> : <Redirect to='/login' />
  },
  {
    path: "/feed",
    exact: true,
    render: ({ isAuthenticated }) => isAuthenticated ? <Feed /> : <Redirect to='/login' />,
  },
  {
    path: "/editRecipe/:id",
    render: ({ isAuthenticated }) => isAuthenticated ? <EditRecipe /> : <Redirect to='/login' />
  },
  {
    path: "/forgetword",
    render: ({ isAuthenticated }) => isAuthenticated ? <Feed /> : <ForgetPassword />
  },
  {
    path: "/recipe/:id?",
    render: ({ isAuthenticated }) => isAuthenticated ? <Recipe /> : <Redirect to='/login' />
  },
  {
    path: "/search",
    component: Search
  }
];

export default routes;
