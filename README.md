This is a python backend project of a cookbook. The cookbook allows authors to log in, create, view, search, edit recipes and visualise stats on the total database contents of recipes. 

The authentication is done with sqlalchemy and using this tutorial as a reference.
https://pythonspot.com/login-authentication-with-flask/

The drag and drop table tutorial for editing the recipe directions is found here:
https://www.html5rocks.com/en/tutorials/dnd/basics/


To install:
1. Install Flask
2. Install SQLAlchemy library
3. Run tabledef.py to setup the database
4. run recipe_server.py to run the application
5. (Optionally) run recipetest.py to test the application



Testing:
I used a build it yourself testing suite in byotest.py. To build the tests, I started with the requirements of the application. Warning: running the tests will clear the database, but I saved a full database at fulldatabase.db, so you can copy and rename it to recipes.db if you accidently delete it by running the tests. I automated as much of the testing as I could, but left these use cases to test mostly the functionality of the UI. 


1. Testing the Register functionality
    a. Run the application
    b. Go to the login page
    c. Enter a new username and password
        i. If succeeded go to login page redirect and check your new name
        ii. If not succeeded read explanation why and redirect back to login page

2. Testing the Login functionality
    a. Follow steps in 1. to create a username
    b. On login page attempt to login with username and password provided.
    c. Attempt to login using a fake username or / and fake password and see if it works

3. Testing the Logout functionality
    a. Follow steps above to login.
    b. Go to the main page when you login and click logout.
    c. This should logout and redirect back to login page again.
