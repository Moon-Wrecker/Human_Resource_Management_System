import { lazy } from "react";
import { createBrowserRouter } from "react-router-dom";
import App from "@/App";

const Home = lazy(() => import("@/pages/Home"));
const Login = lazy(() => import("@/pages/Login"));
const Employee = lazy(() => import("@/layouts/Employee"));
const EmployeeDashboard = lazy(() => import("@/pages/EmployeeDashboard"));

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Home />,
      },
    ],
  },
  { path: "/login", element: <Login /> },
  {
    path: "/employee",
    element: <Employee />,
    children: [
      {
        index: true,
        element: <EmployeeDashboard />,
      },
    ],
  },
]);

export default router;
