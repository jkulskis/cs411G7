import React from 'react';
import {Link } from "react-router-dom";
import './App.css';

function Page4() {
    return(
    <form action="/request" method="POST">
        <div className="container">
            <center><h1>Playlist Generator for Name</h1></center>
            <br />
            <br />
            <hr></hr>
            <p>Here is the playlist we made for you.</p>
            <br /> 
            <p>Click on the button below to listen to your playlist in Spotify.</p>
            <br /> 
            <center><Link to="/page4"><button className="button">My Playlist
            </button></Link></center>
            <br /> 
            <p>If you want to make another playlist, click on the button below to start over.</p>
            <br />
            <center><Link to="/page1"><button className="button">Start Over
            </button></Link></center>
        </div>
    </form>
    );
}

export default Page4;