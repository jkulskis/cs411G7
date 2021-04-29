import React, { Component } from "react";
import { Link, useHistory } from "react-router-dom";
import "./App.css";

function Home() {
  const history = useHistory();
  // note: idk how "correct" this code is, I've never really used react. This is just showing an example of how we fetch data
  // from the login entry point of the API. For other pages (like origin/destination, speed, mode of transport) we
  // will do a post request to send that information to the server, where it can be stored until we do a request to
  // create the playlist
  async function loginButton() {
    return fetch("/login", {
      method: "GET",
    })
      .then((response) => {
        if (response.status === 401) {
          // not logged in yet
          return response.json();
        } else if (response.status === 200) {
          // logged in already
          history.push("/page1");
          return response.json();
        } else {
          console.log("Error");
        }
      })
      .then((data) => {
        if (data && "auth_url" in data) {
          // open auth url popup
          let windowref = window.open(
            data.auth_url,
            "Login with Spotify",
            "width=800,height=800"
          );
          // this is definitely a hacky way to do this...but this will check if the window
          // is closed every 0.5s, and if it has closed then it will check if we are logged in.
          // If we are, then it brings us to the next page. Otherwise, it just reloads the home page
          var timer = setInterval(function () {
            if (windowref.closed) {
              clearInterval(timer);
              fetch("/login", {
                method: "GET",
              }).then((response) => {
                if (response.status === 401) {
                  // Not logged in still...reload page
                  window.location.reload(false);
                } else if (response.status === 200) {
                  // logged in already
                  return response.json()
                } else {
                  console.log("Error");
                }
              }).then((data) => {
                if (data) { // if we passed data, then response was 200, has display_name
                  localStorage.clear();
                  localStorage.setItem("display_name", data.display_name);
                  console.log(localStorage);
                  history.push("/page1");
                }
              });
            }
          }, 500);
        } else if (data) {
          localStorage.clear();
          localStorage.setItem("display_name", data.display_name);
          console.log(localStorage);
        }
      });
  }
  return (
    <div className="container">
      <center>
        <h1>Playlist Generator</h1>
      </center>
      <br />
      <hr></hr>
      <p>
        {" "}
        Discover new music by creating a custom Spotify playlist based on your
        favourite tracks.
      </p>
      <br />
      <p> Login with Spotify to start making a playlist:</p>
      <br />
      <center>
        <button onClick={loginButton} className="button">
          Get Started
        </button>
      </center>
    </div>
  );
}

export default Home;
