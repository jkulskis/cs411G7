import React, { useState, useEffect } from 'react';
import { Link, useHistory} from "react-router-dom";
import './App.css';
import {Form, Button} from 'semantic-ui-react';

function Page3() {


    const [speed, setSpeed] = useState("");
    const history = useHistory();

    useEffect(() => {
        document.title = "Speed"
        if (localStorage["speed"]) speedClicked(localStorage["speed"]);
    }, []);

    let speedClicked = ((speedVal) => {
        if (speed && speed !== speedVal) // check if there was a speed clicked previously, and remove highlight if there was
            document.getElementById(speed).classList.remove("clicked"); // remove previous "clicked" class from other button
        document.getElementById(speedVal).classList.add("clicked"); // add "clicked" class to highlight green
        setSpeed(speedVal);
        localStorage["speed"] = speedVal;
    });

    return (
        <Form>
            <div className="container">
            <center><h1>Welcome {localStorage["display_name"]}!</h1></center>
            <br />
            <center><h2>What's your speed?</h2></center>
            <br />
            <hr></hr>
            <label id="errorLabel"></label>
            <br />
            <label>
                Desired Speed: 
            </label>
            <br></br>
            <br></br>
            <Form.Field>
                <button type="buttonforms" className="buttonforms" value="slower" id="slower" onClick={e => speedClicked(e.target.id)}>Slower</button>
                <button type="buttonforms" className="buttonforms" value="normal" id="normal" onClick={e => speedClicked(e.target.id)}>Normal</button>
                <button type="buttonforms" className="buttonforms" value="faster" id="faster" onClick={e => speedClicked(e.target.id)}>Faster</button>
            </Form.Field>
            <br></br>
            <br></br>        
            <br></br>
            <br></br>
            <Link to="/page2"><button className="buttonback"> Go Back </button></Link>
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
                }).then(function (res) {
                    if (res.status === 401) { // logged out, go back to logic page
                        localStorage["loggedOut"] = "1";
                        history.push("/");
                    }
                    else if (res.status === 400) {
                        document.getElementById("errorLabel").innerHTML = "Please choose a speed to continue";
                        document.getElementById("errorLabel").classList.add("errorText");
                    }
                    else if (res.status === 200) {
                        history.push("/page4");
                        return(res.json());
                    }
                })
                // .then(function (r) {console.log(r)})
            }} className="button"> 
                Next Page
            </Button>
            </div>
        </Form>
    );
}

export default Page3;