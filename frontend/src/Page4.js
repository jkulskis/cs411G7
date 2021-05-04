import React, { useEffect } from 'react';
import { Link } from "react-router-dom";
import './App.css';
import {Form, Button} from 'semantic-ui-react';

function Page4() {

    useEffect(() => {
        document.title = "Playlist"
     }, []);

    var url = ""

    useEffect(() => {
        const response = async () => {
            await fetch('/playlist', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            }).then(function (res) {return(res.json())})
            .then(function (r) {url = r.playlist.external_urls.spotify})
        }
        response()
        console.log(response())
    }, []);

    async function playlistButton() {
        window.open(url)
    }
    console.log(playlistButton)

    return (
        <Form>
            <div className="container">
            <center><h1>Playlist Generator for {localStorage["display_name"]}</h1></center>
            <br />
            <br />
            <hr></hr>
            <h2>Here is the playlist we made for you.</h2>
            <br /> 
            <p>Click on the button below to listen to your playlist in Spotify.</p>
            <br />
                <Button 
                    onClick= {playlistButton}
                    className="button"> 
                    My Playlist
                </Button>
            <br />
            <br />         
            <p>If you want to make another playlist, click on the button below to start over.</p>
            <br />
            <center><Link to="/page1">
                <button className="buttonstartover">Start Over</button></Link>
            </center>
            </div>
        </Form>
    );
}

export default Page4;