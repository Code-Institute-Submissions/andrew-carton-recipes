
// This function searches the database by allergen
function searchByAllergen() {
    var allergenid = document.getElementById("allergen");

    // If the value is empty, just redirect back to recipe page for full listing
    if (allergenid.value == '') {
        window.location.replace("listrecipes");
        return;
    }
    // The URL with an attribute to send to backend
    var sstr = "/searchexcludeallergen?allergen=";

    // New AJAX request
    var xmlhttp = new XMLHttpRequest(); 

    // Append the allergen value
    sstr += allergenid.value;


    xmlhttp.onreadystatechange = function () {
        // On success
        if (this.readyState == 4 && this.status == 200) {
            // Deserialise the data
            var data = JSON.parse(this.responseText);
            // Get the recipes div to add the data to
            var recipesdiv = document.getElementById("recipes");

            var str = '<div class="row">'

            // Add the cards with the data
            for (var i = 0; i < data.length; i++) {
                str += '<div class="col-sm-4 mb-3">';
                str += '<div class="card" style="width: 18rem;">';
                str += '<img class="card-img-top" src="static/images/';
                str += '' + data[i].image + '" height="20%" width="20%">';
                str += '<div class="card-body">';
                str += ' <h5 class="card-title myfont">' + data[i].name + '</h5>';
                str += '<p class="card-text myfont">A ';
                str += '' + data[i].course + ' ' + data[i].country + ' dish ' + ' </p>';
                str += ' <a href="recipe?id=' + data[i].id + '" class="btn btn-primary myfont">View Recipe</a>';
                str += '</div>';
                str += '</div>';
                str += '</div>';

            }
            str += "</div>";
            // Set the div to the list of cards
            recipesdiv.innerHTML = str;
        }
    };
    // AJAX GET of URL
    xmlhttp.open("GET", sstr, true);
    xmlhttp.send();
}

// This function searches by ingredient
function searchByIngredient() {
    // Get the ingredient
    var ingredientid = document.getElementById("ingredient");

    // If empty - give full listing again
    if (ingredientid.value == '') {
        window.location.replace("listrecipes");
        return;
    }

    // String for AJAX Get with attribute
    var sstr = "/searchbyingredient?ingredient=";

    // AJAX request
    var xmlhttp = new XMLHttpRequest();
    // concat value of ingredient to URL 
    sstr += ingredientid.value;
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // On success

            // deserialise JSON into data
            var data = JSON.parse(this.responseText);
            // Get where to insert data
            var recipesdiv = document.getElementById("recipes");

            var str = '<div class="row">'

            // Place data into boostrap cards
            for (var i = 0; i < data.length; i++) {
                str += '<div class="col-sm-4 mb-3">';
                str += '<div class="card" style="width: 18rem;">';
                str += '<img class="card-img-top" src="static/images/';
                str += '' + data[i].image + '" height="20%" width="20%">';
                str += '<div class="card-body">';
                str += ' <h5 class="card-title myfont">' + data[i].name + '</h5>';
                str += '<p class="card-text myfont">A ';
                str += '' + data[i].course + ' ' + data[i].country + ' dish ' + ' </p>';
                str += ' <a href="recipe?id=' + data[i].id + '" class="btn btn-primary myfont">View Recipe</a>';
                str += '</div>';
                str += '</div>';
                str += '</div>';

            }
            str += "</div>";
            // Set data in div
            recipesdiv.innerHTML = str;
        }
    };
    // AJAX GET
    xmlhttp.open("GET", sstr, true);
    xmlhttp.send();
}

// Function to search by course
function searchByCourse() {
    // Get course to search for
    var courseid = document.getElementById("course");

    // IF empty - give full listing again
    if (courseid.value == '') {
        window.location.replace("listrecipes");
        return;
    }

    // URL with attribute to send
    var sstr = "/searchbycourse?course=";

    // New AJAX request
    var xmlhttp = new XMLHttpRequest();
    
    // Append course search to end of URL
    sstr += courseid.value;

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // On Success

            // Deserialise JSON data from backend
            var data = JSON.parse(this.responseText);
            // Get div to insert data
            var recipesdiv = document.getElementById("recipes");
            var str = '<div class="row">'

            // Create data with cards
            for (var i = 0; i < data.length; i++) {
                str += '<div class="col-sm-4 mb-3">';
                str += '<div class="card" style="width: 18rem;">';
                str += '<img class="card-img-top" src="static/images/';
                str += '' + data[i].image + '" height="20%" width="20%">';
                str += '<div class="card-body">';
                str += ' <h5 class="card-title myfont">' + data[i].name + '</h5>';
                str += '<p class="card-text myfont">A ';
                str += '' + data[i].course + ' ' + data[i].country + ' dish ' + ' </p>';
                str += ' <a href="recipe?id=' + data[i].id + '" class="btn btn-primary myfont">View Recipe</a>';
                str += '</div>';
                str += '</div>';
                str += '</div>';

            }
            str += "</div>";
            // Insert data into table
            recipesdiv.innerHTML = str;
        }
    };
    // AJAX get request
    xmlhttp.open("GET", sstr, true);
    xmlhttp.send();
}

