function searchByAllergen() {
    var allergenid = document.getElementById("allergen");
    if (allergenid.value == '') {
        window.location.replace("listrecipes");
        return;
    }
    var sstr = "/searchexcludeallergen?allergen=";

    var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
    sstr += allergenid.value;
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            var recipesdiv = document.getElementById("recipes");
            var str = '<div class="row">'


            for (var i = 0; i < data.length; i++) {
                str += '<div class="col-sm-4 mb-3">';
                str += '<div class="card" style="width: 18rem;">';
                str += '<img class="card-img-top" src="static/images/';
                str += '' + data[i].image + '" height="20%" width="20%">';
                str += '<div class="card-body">';
                str += ' <h5 class="card-title">' + data[i].name + '</h5>';
                str += '<p class="card-text">A ';
                str += '' + data[i].course + ' ' + data[i].country + ' dish ' + ' </p>';
                str += ' <a href="recipe?id=' + data[i].id + '" class="btn btn-primary">View Recipe</a>';
                str += '</div>';
                str += '</div>';
                str += '</div>';

            }
            str += "</div>";
            recipesdiv.innerHTML = str;
        }
    };
    xmlhttp.open("GET", sstr, true);
    xmlhttp.send();
}

function searchByIngredient() {
    var ingredientid = document.getElementById("ingredient");
    if (ingredientid.value == '') {
        window.location.replace("listrecipes");
        return;
    }
    var sstr = "/searchbyingredient?ingredient=";

    var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
    sstr += ingredientid.value;
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            var recipesdiv = document.getElementById("recipes");

            var str = '<div class="row">'


            for (var i = 0; i < data.length; i++) {
                str += '<div class="col-sm-4 mb-3">';
                str += '<div class="card" style="width: 18rem;">';
                str += '<img class="card-img-top" src="static/images/';
                str += '' + data[i].image + '" height="20%" width="20%">';
                str += '<div class="card-body">';
                str += ' <h5 class="card-title">' + data[i].name + '</h5>';
                str += '<p class="card-text">A ';
                str += '' + data[i].course + ' ' + data[i].country + ' dish ' + ' </p>';
                str += ' <a href="recipe?id=' + data[i].id + '" class="btn btn-primary">View Recipe</a>';
                str += '</div>';
                str += '</div>';
                str += '</div>';

            }
            str += "</div>";

            recipesdiv.innerHTML = str;
        }
    };
    xmlhttp.open("GET", sstr, true);
    xmlhttp.send();
}

function searchByCourse() {
    var courseid = document.getElementById("course");
    if (courseid.value == '') {
        window.location.replace("listrecipes");
        return;
    }
    var sstr = "/searchbycourse?course=";

    var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
    sstr += courseid.value;
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            var recipesdiv = document.getElementById("recipes");
            var str = '<div class="row">'


            for (var i = 0; i < data.length; i++) {
                str += '<div class="col-sm-4 mb-3">';
                str += '<div class="card" style="width: 18rem;">';
                str += '<img class="card-img-top" src="static/images/';
                str += '' + data[i].image + '" height="20%" width="20%">';
                str += '<div class="card-body">';
                str += ' <h5 class="card-title">' + data[i].name + '</h5>';
                str += '<p class="card-text">A ';
                str += '' + data[i].course + ' ' + data[i].country + ' dish ' + ' </p>';
                str += ' <a href="recipe?id=' + data[i].id + '" class="btn btn-primary">View Recipe</a>';
                str += '</div>';
                str += '</div>';
                str += '</div>';

            }
            str += "</div>";
            recipesdiv.innerHTML = str;
        }
    };
    xmlhttp.open("GET", sstr, true);
    xmlhttp.send();
}