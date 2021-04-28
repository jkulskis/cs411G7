import React from "react";
import { Link } from "react-router-dom";
import "./App.css";

function Page3() {
  return (
    <form action="/request" method="POST">
      <div className="container">
        <center>
          <h1>Welcome {localStorage.display_name}!</h1>
        </center>
        <br />
        <center>
          <h2>Input the following information</h2>
        </center>
        <br />
        <hr></hr>
        <label>Desired Speed:</label>
        <select>
          <option value="Desired Speed">Desired Speed</option>
          <option value="Slow">Slow</option>
          <option value="Normal">Normal</option>
          <option value="Fast">Fast</option>
        </select>
        <br />
        <br />

        <center>
          <Link to="/page4">
            <button className="button">Submit</button>
          </Link>
        </center>
      </div>
    </form>
  );
}

export default Page3;
