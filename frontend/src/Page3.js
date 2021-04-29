import React from 'react';
import {Link } from "react-router-dom";
import './App.css';

function Page3() {
    return(
    <form action="/request" method="POST">
        <div className="container">
            <center><h1>Welcome name !</h1></center>
            <br />
            <center><h2>What's your speed?</h2></center>
            <br />
            <hr></hr>
            <label>
                Desired Speed:
            </label>
                <br></br>
                <br></br>
            <input type="buttonforms" class="buttonforms" value="Slow"></input>
            <input type="buttonforms" class="buttonforms" value="Normal"></input>
            <input type="buttonforms" class="buttonforms" value="Fast"></input>
                <br></br>
                <br></br>        
                <br></br>
                <br></br>
{/*             <select>
                <option value="Desired Speed">Desired Speed</option>
                <option value="Slow">Slow</option>
                <option value="Normal">Normal</option>
                <option value="Fast">Fast</option>
            </select>
        <br /><br /> */}
        
        <center>
            <Link to="/page2"><button className="buttonback"> Go Back </button></Link>
            <Link to="/page4"><button className="button"> Next Page </button></Link>
        </center>       
            </div>
    </form>
    );
}

export default Page3;