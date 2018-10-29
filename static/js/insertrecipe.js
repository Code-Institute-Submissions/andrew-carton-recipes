var ingnum = 1;
var ingrlist = [];

function send() {
    var form_data = new FormData($('#upload-file')[0]);
    var x = form_data.get('file');

    $.ajax({
        url: "/uploadajax",
        type: "POST",
        data: form_data,
        processData: false,
        contentType: false,
    });
    var id = document.getElementById("myimage");
    id.innerHTML = '<img src="/static/images/' + x.name + '" />';
}

function addIngredient() {
    var id = document.getElementById("ingredient");
    var aid = document.getElementById("allergen");
    var tid = document.getElementById("ingredient_table");
    var amid = document.getElementById("amount");


    var ingobj = new Object();
    ingobj.ingredient = id.value;
    ingobj.allergen = aid.value;
    ingobj.amount = amid.value;
    ingrlist = ingrlist.concat(ingobj);
    tid.innerHTML += "<tr><td>" + ingnum++ + "</td><td>" + id.value + "</td><td>" + amid.value + "</td><td>" + aid.value + "</td></tr>";
    id.value = '';
    aid.value = '';
    amid.value = '';
}

var dirnum = 1;
var dirlist = [];

function addDirection() {
    var id = document.getElementById("direction");

    var tid = document.getElementById("directions_table");
    tid.innerHTML += "<tr><td>" + dirnum++ + "</td><td>" + id.value + "</td></tr>";
    var dirobj = new Object();
    dirobj.direction = id.value;
    dirlist = dirlist.concat(dirobj);
    id.value = '';

}

function submit() {

    var ingrObj = new Object();

    ingrObj.name = document.getElementById("recipename").value;
    ingrObj.country = document.getElementById("country").value;
    ingrObj.course = document.getElementById("course").value;
    ingrObj.author = document.getElementById("author").value;
    ingrObj.ingredients = ingrlist;
    ingrObj.directions = dirlist;
    var form_data = new FormData($('#upload-file')[0]);
    var x = form_data.get('file');

    ingrObj.image = x.name

    var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
    xmlhttp.open("POST", "/insertrecipe");
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.send(JSON.stringify(ingrObj));


    alert("Thank you for submitting the " + ingrObj.name + " recipe!");
    window.location.replace("/listrecipes");

}