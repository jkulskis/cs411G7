import React, { useState, useEffect } from 'react';
import { Link, useHistory} from "react-router-dom";
import './App.css';
import {Form, Button} from 'semantic-ui-react';

function Page2() {

    const [mot, setMot] = useState("");
    const history = useHistory();

    useEffect(() => {
        document.title = "Transportation"
        localStorage["speed"] = ""; // reset speed value in case we went back
        if (localStorage["mot"]) motClicked(localStorage["mot"]);
    }, []);

    let motClicked = ((motVal) => {
        if (mot && mot !== motVal) // check if there was a mot clicked previously, and remove highlight if there was
            document.getElementById(mot).classList.remove("clicked"); // remove previous "clicked" class from other button
        document.getElementById(motVal).classList.add("clicked"); // add "clicked" class to highlight green
        setMot(motVal);
        localStorage["mot"] = motVal;
    });

    return (
        <Form>
            <div className="container">
            <center><h1>Welcome {localStorage["display_name"]}!</h1></center>
            <br />
            <center><h2>How are you getting there?</h2></center>
            <br />
            <hr></hr>
            <label id="errorLabel"></label>
            <br />
            <label>
                Mode of Transportation: 
            </label>
            <br></br>
            <br></br>
            <Form.Field>
                <button type="buttonforms" className="buttonforms" value="walking" id="walking" onClick={e => motClicked(e.target.id)}>Walking</button>
                <button type="buttonforms" className="buttonforms" value="biking" id="biking" onClick={e => motClicked(e.target.id)}>Biking</button>
                <button type="buttonforms" className="buttonforms" value="driving" id="driving" onClick={e => motClicked(e.target.id)}>Driving</button>
            </Form.Field>
            <br></br>
            <br></br>        
            <br></br>
            <br></br>
            <Link to="/page1"><button className="buttonback"> Go Back </button></Link>
            <Button 
            onClick={async () => {
                let data = {mot:mot};
                await fetch('/mot', {
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
                        document.getElementById("errorLabel").innerHTML = "Please choose a mode of transportation to continue";
                        document.getElementById("errorLabel").classList.add("errorText");
                    }
                    else if (res.status === 200) {
                        history.push("/page3");
                        return(res.json());
                    }
                })
            }} className="button"> 
                Next Page
            </Button>
            </div>
        </Form>
    );
}

export default Page2;