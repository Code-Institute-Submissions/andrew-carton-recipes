This is a python full-stack project of a cookbook. The cookbook allows authors to log in, create, view, search, edit recipes and visualise stats on the total database contents of recipes. 

The authentication is done with sqlalchemy and using this tutorial as a reference.
https://pythonspot.com/login-authentication-with-flask/

The drag and drop table tutorial for editing the recipe directions is found here:
https://www.html5rocks.com/en/tutorials/dnd/basics/

The UX Design:

The UX Design will consider the why, what and how of the product use.

The motivation of the user to use the product is to maintain a cookbook or collection of recipes. The functionality of the product includes a user being able to register and log in to insert recipes. Additionally, any user should be able to view the full cookbook of recipes at a glance and to be able to do a search across the cookbook of recipes, using an ingredient, a course (e.g. starter or main), or excluding an allergen (e.g. dairy). The user should also be able to view a visualisation of statistics on current recipes in the cookbook. To achieve this goal, the UX design encompasses the entire user journey, across the requirements of the application, using wireframes to illustrate the design decisions. The design across all of the web site should be user-centered, and focus on the user and provide ease of use of the website - creating a positive user experience without features that necessary surprise the user negatively. Information must be displayed in an organised manner and the web site and it's layout should be intuitive and provide a solution to the users demands. 

The wireframes are illustrated in the ui folder and are designed using an application called Pencil.

The front page (wireframe front-page.png in ui folder) is the first presentation to the user of the web site, as the home page. The home page should provide a warm, friendly feeling to the user and invite the user into the website to explore further. To achieve this end, a colourful background image of a cooking related topic is presented and is persisted across the visit to the website. The background colours are dark colours, and a color scheme for the nav bar and footer are allocated according to these colours. The navigation bar is coloured in black with white coloured text, which is a scheme adopted throughout the rest of website too. The navigation bar invites the user to log in or register along the right-hand side, and further allows them to navigate the rest of the website, including the recipes and the graphs pages. The navigation bar also adapts to a mobile navigation bar depending on the user's device. The main appealing feature of the front page is a carousel - which rotates the different recipe images in the cookbook collection. This feature has a psychological effect on the user, illustrating the tempting visual array of recipes and invites them to explore further the website. 

The recipes page (wireframe recipes-page.png in ui folder) is the main web page and is designed to be as user-centered and user-friendly as possible, with an intuitive feel where the user just 'knows' how to use it by looking at it at a glance. To achieve this end, the search feature of the website is presented in a container around a box, in a standard way, that allows the user to see the search options available at a glance. These options include search by course, ingredient or exclude allergen. The text boxes and search boxes are presented clearly to the user, so it is obvious how this page works. These search options narrow the recipes listed in the main page. The main presentation of this page of course is the recipes list, and this information is presented in an organised manner. Each recipe is given a particular 'card' or 'box' around which it presents the visual and textual information of what it is at a glance. The View button underneath the recipe image, invites the user to investigate that recipe further and redirects to that particular recipe that illustrates more information about it. The number of recipe 'cards' or 'boxes' on the website expands and shrinks according to the users screen, and this allows easy navigation and presentation to users with smaller screens on mobile devices.

The recipe page (wireframe recipe-page.png in the ui folder) is the recipe details page that presents a recipe that the user clicked on from the recipes-page. The recipe page presents the details of the recipe, including the course, country, author, views, image, ingredient list and direction list. This page is important to provide an appealing and easy to read presentation of that recipe. The image of the recipe is presented to the left with the ingredient list to the right hand side and directions of the recipe underneath. In mobile websites, all this information is presented vertically to fit smaller screens. The buttons 'Edit' 'Save' and 'Delete' are displayed at the top left of the recipe page. These buttons allow the user to easily edit the recipe or delete it. When deleting a recipe, a user prompt is displayed to confirm deletion in case it is clicked by accident. The Edit button adds features to the web site that directs the user to be able to edit the recipe. Every effort was made to present a user-centered, friendly and intuitive means to allow the user to achieve this end. Small red x marks are presented beside the ingredients and directions lists upon editing, to allow the user to delete an individual ingredient or direction respectively. Labels and buttons are also added to prompt the user to add further ingredients or directions to the tables presented. Finally, the directions table has a drag-and-drop feature, that allows to user to re-order the table by drag and dropping each direction over another to replace it.

The insert page (wireframe insert-page.png in the ui folder) is the recipe insert page that allows a user to insert a recipe, once he or she is logged in. This option becomes available in the navigation bar once the user is logged in. This page presents three sections to the user. The first section prompts the user to add the main recipe details including the recipe name, country, course, author and an image of the recipe. The second section is a table of ingredients that the user can add to the recipe. The third section is the directions list that the user can add instructions for the recipe into the table. 

The graphs page (wireframe graphs-page.png in the ui folder) is the graph page that allows a user to view the statistics of the cookbook and it's recipes in a visual format. There are three graphs displaying important statistic information to the user. These are course, allergen and country statistics. These graphs reflect the contents of the cookbook and update (upon a revisit) when the user adds or deletes recipes to the cookbook.



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
3. The proc file should take care of the installers
4. run recipeserver.py to run the application
5. (Optionally) run testing/recipetest.py unittest to test the application


Heroku Deployment: https://cookbookproj.herokuapp.com


## Credits

### Content

The recipes were retrived from a script from a REST backend at https://www.themealdb.com/


### Acknowledgements

