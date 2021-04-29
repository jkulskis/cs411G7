import React from 'react';
import {Link } from "react-router-dom";
import './App.css';

function Home() {
    return(
    <form action="/request" method="POST">
        <div className="container">
            <center><h1>Playlist Generator</h1></center>
            <br />
            <hr></hr>
            <p> Discover new music by creating a custom Spotify playlist based on your favourite tracks.</p>
            <br />
            <p> Login with Spotify to start making a playlist:</p>
            <br />
            <center><Link to="/page1"><button className="button">Get Started
            </button></Link></center>
        </div>
    </form>
    );
}

export default Home;

