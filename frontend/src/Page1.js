import React from "react";
import {Link } from "react-router-dom";
import './App.css';

function Page1() {
    return (
    <form action="/request" method="POST">
        <div className="container">
        <center><h1>Welcome name !</h1></center>
        <br />
        <center><h2>Input the following information</h2></center>
        <br />
        <hr></hr>
        <label> Current Location: </label>
        <input type="text" name="origin" placeholder= "Current Location" size="15" required />
        <label> Destination: </label>
        <input type="text" name="destination" placeholder="Destination" size="15" required />

        <center><Link to="/page2"><button className="button">Next
            </button></Link></center>
  
        </div>
    </form>
    );
}

export default Page1;