import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "../Components/Navbar/Navbar";

function Layout() {
  return (
    <>
      <Outlet />
      <Navbar />
    </>
  );
}

export default Layout;
