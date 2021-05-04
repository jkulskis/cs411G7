import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import './App.css';
import {Form, Button} from 'semantic-ui-react';

function Page2() {

    useEffect(() => {
        document.title = "Transportation"
     }, []);

    const [mot, setMot] = useState("");

    return (
        <Form>
            <div className="container">
            <center><h1>Welcome {localStorage["display_name"]}!</h1></center>
            <br />
            <center><h2>How are you getting there?</h2></center>
            <br />
            <hr></hr>
            <label>
                Mode of Transportation: 
            </label>
            <br></br>
            <br></br>
            <Form.Field>
                <button type="buttonforms" className="buttonforms" value="walking" onClick={e => setMot(e.target.value)}>Walking</button>
                <button type="buttonforms" className="buttonforms" value="biking" onClick={e => setMot(e.target.value)}>Biking</button>
                <button type="buttonforms" className="buttonforms" value="driving" onClick={e => setMot(e.target.value)}>Driving</button>
            </Form.Field>
            <br></br>
            <br></br>        
            <br></br>
            <br></br>
            <Link to="/page1"><button className="buttonback"> Go Back </button></Link>
            <Link to="/page3">
                <Button 
                onClick={async () => {
                    let data = {mot:mot};
                    console.log(data)
                    await fetch('/mot', {
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

export default Page2;