import React from 'react';
import {Link } from "react-router-dom";
import './App.css';

function Page2() {
    return (
    <form action="/request" method="POST">
        <div className="container">
        <center><h1>Welcome name !</h1></center>
        <br />
        <center><h2>How are you getting there?</h2></center>
        <br />
        <hr></hr>
        <label>
        Mode of Transportation: 
        </label>
        <br></br>
        <br></br>

        <input type="buttonforms" class="buttonforms" value="Walking"></input>
        <input type="buttonforms" class="buttonforms" value="Biking"></input>
        <input type="buttonforms" class="buttonforms" value="Driving"></input>

{/*         <select>
            <option value=" "> </option>
            <option value="Walking" class="buttonforms">Walking</option>
            <option value="Biking" class="buttonforms">Biking</option>
            <option value="Driving" class="buttonforms">Driving</option>
        </select>
        <br /><br /> */}
        <br></br>
        <br></br>        
        <br></br>
        <br></br>
        
        <center>
            <Link to="/page1"><button className="buttonback"> Go Back </button></Link>
            <Link to="/page3"><button className="button"> Next Page </button></Link>
        </center>

        </div>
    </form>
    );
}

export default Page2;