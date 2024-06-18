# Quiz-Tool

Welcome to Quiz-tool! This project creates a website where users can signup/login to give quiz on computer-science questions. The questions are divided into easy, mdeium and hard levels and they are scored accordingly. The questions are scrapped from live websites and are stored on Mongo DataBase for further use.

## Overview 

This project is aimed at building a website that can generate quizzes for students on the subject of computer science. The questions are scraped from live websites to avoid the overuse and aging away of questions.

### Questions 

The questions are scraped from the links for quizzes given on the following webpage - https://www.geeksforgeeks.org/quiz-corner-gq/. The webscrapping process is done with the help of Selenium. They are then divided into groups based on difficulties - Easy, Medium and Hard. This can be changed by the admin as deemed fit.

## Creating Webpages

The main languages used for creating these webpages were HTML and CSS. To handle and display errors, Jinja2 framework was used. It is highly resourceful for including messages and errors passed from the backend to be used and displayed in the frontend portion/on the webpage.

## Account Access

 - User account - 
 For a normal user, they are only permissible to create their account, login, give tests and see their results on the userpage. They cannot access the admin page/dashboard. The about us and contact us pages are accessible by all.

- Admin account - 
The admin has access to the database questions that are displayed on a webpage where the admin can change their difficulty level as required. This will directly make changes to the database. The admin is also provided with a button to get new questions from the links or scrape the questions currently present on the live website.

## Flask Framework 

Flask is the main framework used in this project for building the website and handling the database. It provides several important functions and classes:

 - Flask Application: The core of the application where routes, configurations, and extensions are defined.
 - Flask Blueprints: Help in organizing the application into modular components, making the codebase more manageable.
 - Jinja2 Templating: Renders dynamic HTML pages, allowing seamless integration of Python code with HTML.
 - Flask-Login: Manages user session and authentication, ensuring secure login and logout functionalities.
 - Flask-PyMongo: Facilitates interaction with MongoDB, simplifying database operations.

## Getting Started 

To get started with the Quiz-Tool project:

  1. Clone the repository to your local machine.
  2. Install dependencies using pip install -r requirements.txt.
  3. Run the app.py file.
  4. Sign up with your username and password.
  5. Give quiz based on your preference of difficulty.

## Support and Feedback 

- For any issues, feedback, or queries related to the Quiz-Tool project, please contact hemangmehta63@gmail.com
