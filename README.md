test users

jason 12345
jemima2 12345

/admin/ admin Password1


# CHATTER 

**Description:** This application is a blog style posting site, used to demonstrate the features available within a flask application and its uses as a database management system. 

## Table of Contents
1. [Project Description](#project-description)
2. [User Stories](#user-stories)
3. [Testing Procedures](#testing-procedures)
4. [Technologies Used](#technologies-used)
5. [Acknowledgements](#acknowledgements)
6. [Libraries Used](#libraries-used)
7. [Security Procedures](#security-procedures)

## Project Description

The User is provided with a registration portal which handles a username/password combination and stores the data securely using mongodb-community. Once authorised the user is directed to a dashboard page which provides a post-view section of posts authored by registered users and a post-form section which acts as a submission function for new posts. The front of the application was developed using HTML/CSS with some slight jQuery functionality, using a flask template which is inherited across login page and dashboard page. The back end of the application is written in python using mongodb as a database management system, holding user data such as login material(username/password), posts authored by user, and the ability to delete these posts from the database. 


## User Stories

### As a Chatter user, I want to create custom posts, so that other users may view my content...

 **As a registered user:**
   - I want to log in securely to access personalized features.
   - I want to create, edit, and delete my blog posts.
   - I want to be able to create and remove posts that exist in a secure database

## Security Procedures

The Chatter application demonstrates several security features that help protect user data and authenticate access to sensitive routes. One key security feature is the use of password hashing for user authentication. The application employs the `generate_password_hash` function from Flask's `werkzeug.security` module when creating a new user. This function securely hashes the user's password before storing it in the database. During the login process, the application uses `check_password_hash` to verify the entered password against the hashed password stored in the database. This approach enhances security by preventing the exposure of plain-text passwords, even in the event of a data breach.

Chatter also integrates Flask-Login to manage user sessions and access control. The `LoginManager` from Flask-Login is initialized and configured to work with the Flask app. The `User` class is defined to represent a user object, and a user loader function (`load_user`) is implemented to retrieve user information from the MongoDB database. This ensures that user authentication is handled securely, and user data is efficiently loaded and stored during login sessions. By using Flask-Login, the application strengthens protection against unauthorized access to routes requiring authentication, like the dashboard and logout routes, as evidenced by the `@login_required` decorator.

---

## Testing Procedures

Testing procedures for this application include writing custom python tests within a tests.py file which allow the author to take separate functions within the application file and systematically check each feature for bugs, such as testing the user registration route. ![RegistrationTest](./assets/images/first-python-test.png)

HTML and CSS properties although not a huge feature of understanding within the MS3/Chatter project were tested through tools such as HTML/CSS Validators and Googles Lighthouse testing environment, providing the author with valuable feedback on how to better structure the applications frontend. ![LighthouseTest](./assets/images/lighthouse-score-dashboard.png)




## Technologies Used

- **Flask:** Python web framework for building the backend, posting and security(login) features.
- **HTML/CSS:** Frontend markup and styling.
- **MongoDB Community:** Database management system for storing and retrieving data.

## Acknowledgements

Jquery
HTML/CSS Validator 
Flask
Werkzeug
Mongodb
Mongo community edition 
bootstrap


## Libraries Used



- **Flask:** Web framework for Python.
- **[Library Name]:** Brief description of the library and its purpose.
- ...