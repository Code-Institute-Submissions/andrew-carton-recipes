// The ingredient position
var ingnum = 1;
// The ingredient list
var ingrlist = [];

// Send the to the backend via AJAX
function send() {
    // The file
    var form_data = new FormData($('#upload-file')[0]);
    var x = form_data.get('file');

    // Ajax post call to backend
    $.ajax({
        url: "/uploadajax",
        type: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (data) {
            // Display image on success
            var id = document.getElementById("myimage");
            id.innerHTML = '<img src="/static/images/' + x.name + '" />';
        }
    });
   
}

// Add Ingredient to ingredient table
function addIngredient() {
    // Get the ingredient data and the table
    var id = document.getElementById("ingredient");
    var aid = document.getElementById("allergen");
    var tid = document.getElementById("ingredient_table");
    var amid = document.getElementById("amount");


    // Create a new object with for specifing an ingredient
    // which is ingredient name, allergen and the amount
    var ingobj = new Object();
    ingobj.ingredient = id.value;
    ingobj.allergen = aid.value;
    ingobj.amount = amid.value;
    // Append it to the collection for later
    ingrlist = ingrlist.concat(ingobj);

    // Add the ingredient and it's data to the table
    tid.innerHTML += "<tr><td class=\"myfont\">" + ingnum++ + "</td><td class=\"myfont\">" + id.value + "</td><td class=\"myfont\">" + amid.value + "</td><td class=\"myfont\">" + aid.value + "</td></tr>";
    // Reset the ingredient data to empty after insert
    id.value = '';
    aid.value = '';
    amid.value = '';
}

// The direction position
var dirnum = 1;
// The direction object list
var dirlist = [];

// Add Direction from form to directions table
function addDirection() {
    // Get Direction and direction table
    var id = document.getElementById("direction");
    var tid = document.getElementById("directions_table");
    
    // Add the direction to the direction table
    tid.innerHTML += "<tr><td class=\"myfont\">" + dirnum++ + "</td><td class=\"myfont\">" + id.value + "</td></tr>";
    
    // Create a new object that holds the direction
    var dirobj = new Object();
    dirobj.direction = id.value;
    // Add to collection
    dirlist = dirlist.concat(dirobj);
    // Reset value of direction to empty after inserting
    id.value = '';

}

// This function submits the recipe from the collections
// and data held
function submit() {

    // Create an object of the recipe
    var ingrObj = new Object();

    // Get the common properties of the recipe data
    ingrObj.name = document.getElementById("recipename").value;
    ingrObj.country = document.getElementById("country").value;
    ingrObj.course = document.getElementById("course").value;
    ingrObj.author = document.getElementById("author").value;
    // Get the collections held from inserting to the tables
    ingrObj.ingredients = ingrlist;
    ingrObj.directions = dirlist;

    // Get the file name
    var form_data = new FormData($('#upload-file')[0]);
    var x = form_data.get('file');

    ingrObj.image = x.name

    // AJAX post request
    var xmlhttp = new XMLHttpRequest(); 
    xmlhttp.open("POST", "/insertrecipe");
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    // Serialise object to JSON and send
    xmlhttp.send(JSON.stringify(ingrObj));

    // Alert the user for submitting the recipe
    alert("Thank you for submitting the " + ingrObj.name + " recipe!");

    // Redirect back to the recipes page
    window.location.replace("/listrecipes");

}