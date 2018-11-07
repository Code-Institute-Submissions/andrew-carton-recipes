
function searchRecipes() {
    var allergenid = document.getElementById("allergen");
    var ingredientid = document.getElementById("ingredient");
    var courseid = document.getElementById("course");

    if (allergenid.value == '' && ingredientid == '' && courseid == '') {
        window.location.replace("listrecipes");
        return;
    }

     // The URL with an attribute to send to backend
     var sstr = "/search?allergen=";

     // New AJAX request
     var xmlhttp = new XMLHttpRequest(); 
 
     // Append the values
     sstr += allergenid.value;

     sstr += "&ingredient=";

     sstr += ingredientid.value;

     sstr += "&course=";

     sstr += courseid.value;
 
 
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
                 str += '<div class="col mb-3">';
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

