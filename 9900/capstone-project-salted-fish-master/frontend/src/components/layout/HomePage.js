import React from "react";
import { Link } from "react-router-dom";

import background1 from "./img1.jpeg";
import background2 from "./img2.jpeg";
import { Parallax } from "react-parallax";

const HomePage = () => {
  return (
    <div>
      <div class="parallax-container">
        <Parallax bgImage={background1} bgImageAlt="the cat" strength={800}>
          <div style={{ height: "500px" }} />
        </Parallax>
      </div>

      <section className="center">
        <h1>Connect Your Dream</h1>
        <p>Find your dream collaborator and get help from others</p>
        <div>
          <Link
            to="register"
            className="btn waves-effect waves-light blue-grey lighten-1"
            style={{ margin: "5px" }}
          >
            Sign Up
          </Link>
          <Link
            to="login"
            className="btn waves-effect waves-light blue-grey lighten-1"
            style={{ margin: "10px" }}
          >
            Login
          </Link>
        </div>
      </section>

      <div class="parallax-container">
        <Parallax bgImage={background2} bgImageAlt="the cat" strength={1000}>
          <div style={{ height: "500px" }} />
        </Parallax>
      </div>

      <div class="container">
        <div class="row">
          <div class="col s12 m4">
            <div class="icon-block">
              <h2 class="center brown-text">
                <i class="material-icons">people</i>
              </h2>
              <h5 class="center">Speeds up collaborator</h5>

              <p class="light">
                FindColla is a community of engineers, designers, project managers, and dreamers.
                Some have good ideas and some have technical know how to turn those dreams into a reality.
              </p>
            </div>
          </div>

          <div class="col s12 m4">
            <div class="icon-block">
              <h2 class="center brown-text">
                <i class="material-icons">bubble_chart</i>
              </h2>
              <h5 class="center">Easy to communicate</h5>

              <p class="light">
                Dreamers and collaborators can communicate with each other easily.
                There are communicate board under each projects and invitation messages
                can be emailed between users.
              </p>
            </div>
          </div>

          <div class="col s12 m4">
            <div class="icon-block">
              <h2 class="center brown-text">
                <i class="material-icons">settings</i>
              </h2>
              <h5 class="center">Good community environment</h5>

              <p class="light">
                Administrator will hide improper projects and supervise dreamers to modify them.
                Hence the community will keep safe, efficient, and professional.
              </p>
            </div>
          </div>
        </div>
      </div>
      <footer className="page-footer blue-grey lighten-1">
          <div className="container center-align">
            <div>© 2020 Copyright Salted-Fish-team</div>
            <div>contact: fishsalted42@gmail.com</div>
            <br/>
        </div>
      </footer>

    </div>
  );
};

export default HomePage;
