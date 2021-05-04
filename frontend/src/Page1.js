import React, { useState, useEffect } from "react";
import { useHistory} from "react-router-dom";
import './App.css';
import {Form, Input, Button} from 'semantic-ui-react';

function Page1() {
    const [destination, setDestination] = useState("");
    const [origin, setOrigin] = useState("");
    const history = useHistory();

    useEffect(() => {
        document.title = "Destination"
        // reset mot and speed values in case we went back
        localStorage["mot"] = ""; 
        localStorage["speed"] = "";
        if (localStorage["origin"]) {
            document.getElementById("origin").value = localStorage["origin"];
            setOrigin(localStorage["origin"]);
        }
        if (localStorage["destination"]) {
            document.getElementById("destination").value = localStorage["destination"];
            setDestination(localStorage["destination"]);
        }
    }, []);
    
    return (
        <Form>
            <div className="container">
            <center><h1>Welcome {localStorage["display_name"]}!</h1></center>
            <br />
            <center><h2>Where are you going?</h2></center>
            <br />
            <hr></hr>
            <label id="errorLabel"></label>
            <br />
            <label> Current Location: </label>
            <Form.Field>
                <Input 
                    id="origin"
                    placeholder="Origin" 
                    value={origin} 
                    onChange={e => setOrigin(e.target.value)}
                    spellCheck="false"
                /> 
            </Form.Field>
            <label> Destination: </label>
            <Form.Field>
                <Input 
                    id="destination"
                    placeholder="Destination" 
                    value={destination} 
                    onChange={e => setDestination(e.target.value)}
                    spellCheck="false"
                /> 
            </Form.Field>
            <Form.Field>
            <Button 
            onClick={async () => {
                let data = {destination:destination, origin:origin};
                console.log(data)
                await fetch('/travel', {
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
                        document.getElementById("errorLabel").innerHTML = "Please enter in valid locations to continue";
                        document.getElementById("errorLabel").classList.add("errorText");
                    }
                    else if (res.status === 200) {
                        history.push("/page2")
                        return(res.json())
                    }
                }).then(
                    (res) => {
                        if (res) {
                            localStorage["origin"] = res.user_choices.origin;
                            localStorage["destination"] = res.user_choices.destination;
                        }
                    }
                );
            }} className="button"> 
                Next
            </Button>
            </Form.Field>
            </div>
        </Form>
    );
}

export default Page1;