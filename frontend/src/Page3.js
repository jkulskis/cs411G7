import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import './App.css';
import {Form, Button} from 'semantic-ui-react';

function Page3() {

    useEffect(() => {
        document.title = "Speed"
     }, []);

    const [speed, setSpeed] = useState("");

    return (
        <Form>
            <div className="container">
            <center><h1>Welcome {localStorage["display_name"]}!</h1></center>
            <br />
            <center><h2>What's your speed?</h2></center>
            <br />
            <hr></hr>
            <label>
                Desired Speed: 
            </label>
            <br></br>
            <br></br>
            <Form.Field>
                <button type="buttonforms" className="buttonforms" value="slower" onClick={e => setSpeed(e.target.value)}>Slower</button>
                <button type="buttonforms" className="buttonforms" value="normal" onClick={e => setSpeed(e.target.value)}>Normal</button>
                <button type="buttonforms" className="buttonforms" value="faster" onClick={e => setSpeed(e.target.value)}>Faster</button>
            </Form.Field>
            <br></br>
            <br></br>        
            <br></br>
            <br></br>
            <Link to="/page2"><button className="buttonback"> Go Back </button></Link>
            <Link to="/page4">
                <Button 
                onClick={async () => {
                    let data = {speed:speed};
                    console.log(data)
                    let sp = speed;
                    console.log(sp)
                    await fetch('/speed', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    }).then(function (res) {return(res.json())})
                    .then(function (r) {console.log(r)})
                }} className="button"> 
                    Next Page
                </Button>
            </Link>
            </div>
        </Form>
    );
}

export default Page3;