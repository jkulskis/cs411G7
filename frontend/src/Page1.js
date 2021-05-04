import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import './App.css';
import {Form, Input, Button} from 'semantic-ui-react';

function Page1() {
    const [destination, setDestination] = useState("");
    const [origin, setOrigin] = useState("");
    
    useEffect(() => {
        document.title = "Destination"
    }, []);
    
    return (
        <Form>
            <div className="container">
            <center><h1>Welcome {localStorage["display_name"]}!</h1></center>
            <br />
            <center><h2>Where are you going?</h2></center>
            <br />
            <hr></hr>
            <label> Current Location: </label>
            <Form.Field>
                <Input 
                    placeholder="Origin" 
                    value={origin} 
                    onChange={e => setOrigin(e.target.value)}
                /> 
            </Form.Field>
            <label> Destination: </label>
            <Form.Field>
                <Input 
                    placeholder="Destination" 
                    value={destination} 
                    onChange={e => setDestination(e.target.value)}
                /> 
            </Form.Field>
            <Form.Field>
            <Link to="/page2">
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
                    }).then(function (res) {return(res.json())})
                    .then(function (r) {console.log(r)})
                }} className="button"> 
                    Next
                </Button>
            </Link>
            </Form.Field>
            </div>
        </Form>
    );
}

export default Page1;