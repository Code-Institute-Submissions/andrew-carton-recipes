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

4. Testing the Recipe List
    a. Go to the recipe list page
    b. The recipes should be listed
    c. click on a recipe to view it
    d. The recipe should be viewed

5. Testing the search recipe
    a. Enter in an item for search by course e.g. main and click submit
    b. The list should filter depending on the submitted value
    c. Try the exact same thing with ingredient and exclude allergen
    d. The list should be filtered simularly

6. Graphs
    a. Go to the graphs page
    b. The graphs should display the relevant information reflecting the recipes present
       from the recipes page
    
    a. Add a recipe with an allergen or course
    b. Check the graph accurately reflects the new data

7. Inserting a recipe
    a. Make sure you are logged in
    b. Go to Insert Recipe page
    c. Add in all the values
    d. Submit a photo if you like and hit upload
    e. Submit the recipe
    f. Go back to recipe list and make sure the recipe is displayed

8. Deleting a recipe
    a. Go to a recipe you want to delete
    b. Hit delete and confirm deletion
    c. Go back to recipe list to see that it is gone

9. Editing a recipe
    a. Go to a recipe
    b. Hit Edit and the edit options appear
    c. Select an item to edit - either course, country, recipe list, ingredient list, or sorting the recipe instruction drop and drag list
    d. Hit Save
    e. Go back to the recipe on the recipe list and see it has changed

## Deployment

To install:
1. Install Flask and Flash-Login
2. Install SQLAlchemy library
3. Run tabledef.py to setup the database
4. run recipeserver.py to run the application
5. (Optionally) run riddletest.py to test the application


Heroku Deployment: https://cookbookproj.herokuapp.com


## Credits

### Content

The recipes were retrived from a script from a REST backend at https://www.themealdb.com/


### Acknowledgements

