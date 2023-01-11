<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ervinteoh/flask-demo-login">
    <img src="images/logo.svg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Flask Demo Login</h3>

  <p align="center">
    A demonstration of an authentication system on a website.
    <br />
    <a href="https://github.com/ervinteoh/flask-demo-login"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://flask-demo-login.onrender.com/">View Demo</a>
    ·
    <a href="https://github.com/ervinteoh/flask-demo-login/issues">Report Bug</a>
    ·
    <a href="https://github.com/ervinteoh/flask-demo-login/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://flask-demo-login.onrender.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][Python-badge]][Python-url]
[![JavaScript][JavaScript-badge]][JavaScript-url]
[![Flask][Flask-badge]][Flask-url]
[![TailwindCSS][TailwindCSS-badge]][TailwindCSS-url]
[![Webpack][Webpack-badge]][Webpack-url]
[![PostgreSQL][PostgreSQL-badge]][PostgreSQL-url]
[![GitHub Actions][GitHubActions-badge]][GitHubActions-url]
[![Docker][Docker-badge]][Docker-url]
[![Render][Render-badge]][Render-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Node Package Management
  ```sh
  npm install npm@latest -g
  ```
* Python

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ervinteoh/flask-demo-login.git
   ```
2. Install NPM packages
   ```sh
   npm ci
   ```
3. Build Static Files
   ```sh
   npm run build
   ```
4. Make a copy of the file `.env.example` and rename it to `.env`
5. Fill in the missing environmental variables in `.env` file
6. Install package requirements
   ```sh
   pip install -r requirements.txt
   ```
7. Database Migration
   ```sh
   flask db upgrade
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Start the web application by simply running the command below.
```sh
flask run
```

To run the web application in debug mode run the following command instead.
```sh
export FLASK_DEBUG=1
flask run
```

Use the following command to find out more about the flask command line interface.
```sh
flask --help
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3

See the [open issues](https://github.com/ervinteoh/flask-demo-login/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Jie Sheng Teoh (Ervin) - teohjies@gmail.com

Project Link: [https://github.com/ervinteoh/flask-demo-login](https://github.com/ervinteoh/flask-demo-login)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [README Template](https://github.com/othneildrew/Best-README-Template)
* [Freepik Illustrations](https://www.freepik.com/search?author=55705010&authorSlug=bs_k1d&format=author)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ervinteoh/flask-demo-login.svg?style=for-the-badge
[contributors-url]: https://github.com/ervinteoh/flask-demo-login/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ervinteoh/flask-demo-login.svg?style=for-the-badge
[forks-url]: https://github.com/ervinteoh/flask-demo-login/network/members
[stars-shield]: https://img.shields.io/github/stars/ervinteoh/flask-demo-login.svg?style=for-the-badge
[stars-url]: https://github.com/ervinteoh/flask-demo-login/stargazers
[issues-shield]: https://img.shields.io/github/issues/ervinteoh/flask-demo-login.svg?style=for-the-badge
[issues-url]: https://github.com/ervinteoh/flask-demo-login/issues
[license-shield]: https://img.shields.io/github/license/ervinteoh/flask-demo-login.svg?style=for-the-badge
[license-url]: https://github.com/ervinteoh/flask-demo-login/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ervinteoh
[product-screenshot]: images/screenshot.png
[Python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[JavaScript-badge]: https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E
[JavaScript-url]: https://www.javascript.com/
[Flask-badge]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[TailwindCSS-badge]: https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white
[TailwindCSS-url]: https://tailwindcss.com/
[Webpack-badge]: https://img.shields.io/badge/webpack-%238DD6F9.svg?style=for-the-badge&logo=webpack&logoColor=black
[Webpack-url]: https://webpack.js.org/
[PostgreSQL-badge]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[GitHubActions-badge]: https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white
[GitHubActions-url]: https://github.com/features/actions
[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Render-badge]: https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white
[Render-url]: https://render.com/
