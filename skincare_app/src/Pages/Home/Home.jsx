import React from "react";
import { check } from "../../services/apicheck";
import Search_Product from "../../Components/Search_Product/Search_Product";
import RoutineInput from "../../Components/RoutineGenerator/RoutineGenerator";

function Home() {
  const handleConnection = async () => {
    await check();
  };
  return (
    <div>
      Home
      <button onClick={handleConnection}>check connection</button>
      <Search_Product />
      <RoutineInput />
    </div>
  );
}

export default Home;
