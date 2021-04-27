import React from 'react';
import {Link } from "react-router-dom";
import './App.css';

function Page2() {
    return (
    <form action="/request" method="POST">
        <div className="container">
        <center><h1>Welcome name !</h1></center>
        <br />
        <center><h2>Input the following information</h2></center>
        <br />
        <hr></hr>
        <label>
        Mode of Transportation: 
        </label>
        <select>
            <option value="Mode of transportation">Mode of transportation</option>
            <option value="Walking">Walking</option>
            <option value="Biking">Biking</option>
            <option value="Driving">Driving</option>
        </select>
        <br /><br />

        <center><Link to="/page3"><button className="button">Next
            </button></Link></center>

        </div>
    </form>
    );
}

export default Page2;