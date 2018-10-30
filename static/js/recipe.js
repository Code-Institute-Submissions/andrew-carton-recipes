function addIngredient() {
    removeRemove();
    var id = document.getElementById("ingredient");
    var aid = document.getElementById("allergen");
    var tid = document.getElementById("ingredients");
    var amid = document.getElementById("amount");



    tid.innerHTML += "<tr><td style=\"padding:0 15px 0 15px;\">" + id.value + "</td><td style=\"padding:0 15px 0 15px;\">" + amid.value + "</td><td style=\"padding:0 15px 0 15px;\">" + aid.value + "</td></tr>";
    id.value = '';
    aid.value = '';
    amid.value = '';
    addRemove();
}


function addDirection() {
    removeRemove();
    var id = document.getElementById("direction");

    var tid = document.getElementById("directions");
    var rows = tid.rows;
    var dirnum = tid.rows.length;
    tid.innerHTML += "<tr draggable=\"true\" class=\"column\" style=\"cursor: move;\"><td style=\"padding:10px 15px 0 15px;\">" + dirnum++ + "</td><td style=\"padding:10px 15px 0 15px;\">" + id.value + "</td></tr>";

    var tid = document.getElementById("directions");
    var rows = tid.rows;



    id.value = '';
    addCallbacks();
    addRemove();
}

var dragSrcEl = null;

function reorder() {
    var table = document.getElementById('directions');

    rows = table.rows;
    for (var i = 0; i < rows.length; i++) {
        rows[i].cells[0].innerHTML = i;
    }
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault(); 
    }

    e.dataTransfer.dropEffect = 'move'; 

    return false;
}

function handleDragEnter(e) {
    this.classList.add('over');

}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault(); 
    }

    e.dataTransfer.dropEffect = 'move'; 

    return false;

}

function handleDragLeave(e) {
    this.classList.remove('over');

}

function handleDragEnd(e) {
    var cols = document.querySelectorAll('#directions .column');
    [].forEach.call(cols, function (col) {
        col.classList.remove('over');
    });
    reorder();
}

function handleDrop(e) {

    if (e.stopPropagation) {
        e.stopPropagation(); // Stops some browsers from redirecting.
    }
    if (dragSrcEl != this) {
        dragSrcEl.innerHTML = this.innerHTML;
        this.innerHTML = e.dataTransfer.getData('text/html');
    }
    removeRemove();
    addRemove();

    return false;
}

function handleDragStart(e) {
    dragSrcEl = this;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}


function removeRemove() {

    var table = document.getElementById('directions');

    rows = table.rows;
    for (var i = 0; i < rows.length; i++) {
        for (var j = 0; j < rows[i].cells.length; j++) {
            if (rows[i].cells[j].innerHTML == 'x') {
                table.rows[i].deleteCell(j);
                break;
            }
        }
    }

    table = document.getElementById('ingredients');

    rows = table.rows;
    for (var i = 0; i < rows.length; i++) {
        for (var j = 0; j < rows[i].cells.length; j++) {
            if (rows[i].cells[j].innerHTML == 'x') {
                table.rows[i].deleteCell(j);
                break;
            }
        }
    }

}

function addRemove() {

    var table = document.getElementById('directions');
    var rows = table.rows;
    for (var i = 0; i < rows.length; i++) {

        cell = rows[i].insertCell(rows[i].cells.length);
        cell.style.color = "red";
        cell.innerHTML = "x";


        cell.addEventListener('mouseover', function (e) {
            this.style.cursor = "pointer";
        }, false);
        cell.addEventListener('click', function (e) {
            var table2 = document.getElementById('directions');
            rows = table2.rows;
            for (var i = 0; i < rows.length; i++) {

                for (var j = 0; j < rows[i].cells.length; j++) {
                    if (rows[i].cells[j] == this) {
                        table2.deleteRow(i);
                        break;
                    }
                }


            }
            reorder();

        }, false);
    }

    var table = document.getElementById('ingredients');
    var rows = table.rows;
    for (var i = 0; i < rows.length; i++) {

        cell = rows[i].insertCell(rows[i].cells.length);
        cell.style.color = "red";
        cell.innerHTML = "x";


        cell.addEventListener('mouseover', function (e) {
            this.style.cursor = "pointer";
        }, false);
        cell.addEventListener('click', function (e) {
            var table2 = document.getElementById('ingredients');
            rows = table2.rows;
            for (var i = 0; i < rows.length; i++) {

                for (var j = 0; j < rows[i].cells.length; j++) {
                    if (rows[i].cells[j] == this) {
                        table2.deleteRow(i);
                        break;
                    }
                }


            }


        }, false);
    }

}

function addDirectionForm() {
    var iform = document.getElementById("directionform");
    f = document.createElement("form");
    f.setAttribute("action", "javascript:addDirection()");
    f.setAttribute("method", "POST");

    i1 = document.createElement("input");
    i1.type = "text";
    i1.id = "direction"
    i1.placeholder = "Direction";
    f.appendChild(i1);


    i4 = document.createElement("input");
    i4.type = "submit";
    i4.class = "btn btn-primary";
    i4.value = "Add Direction";
    f.appendChild(i4);


    iform.appendChild(f);
}

function addCourseForm() {
    var iform = document.getElementById("courseform");
    f = document.createElement("form");
    f.setAttribute("action", "");
    f.setAttribute("method", "POST");

    i1 = document.createElement("input");
    i1.type = "text";
    i1.id = "course"
    i1.value = recipeCourse;
    f.appendChild(i1);

    iform.appendChild(f);
}

function addCountryForm() {
    var iform = document.getElementById("countryform");
    f = document.createElement("form");
    f.setAttribute("action", "");
    f.setAttribute("method", "POST");

    i1 = document.createElement("input");
    i1.type = "text";
    i1.id = "country"
    i1.value = recipeCountry;
    f.appendChild(i1);

    iform.appendChild(f);
}

function addIngredientForm() {
    var iform = document.getElementById("ingredientform");
    f = document.createElement("form");
    f.setAttribute("action", "javascript:addIngredient()");
    f.setAttribute("method", "POST");

    i1 = document.createElement("input");
    i1.type = "text";
    i1.id = "ingredient"
    i1.placeholder = "Ingredient";
    f.appendChild(i1);

    i2 = document.createElement("input");
    i2.type = "text";
    i2.id = "amount"
    i2.placeholder = "Amount";
    f.appendChild(i2);

    i3 = document.createElement("input");
    i3.type = "text";
    i3.id = "allergen"
    i3.placeholder = "Allergen";
    f.appendChild(i3);

    i4 = document.createElement("input");
    i4.type = "submit";
    i4.class = "btn btn-primary";
    i4.value = "Add Ingredient";
    f.appendChild(i4);


    iform.appendChild(f);
}

function addCallbacks() {
    var cols = document.querySelectorAll('#directions .column');
    [].forEach.call(cols, function (col) {

        col.addEventListener('dragstart', handleDragStart, false);
        col.addEventListener('dragenter', handleDragEnter, false);
        col.addEventListener('dragover', handleDragOver, false);
        col.addEventListener('dragleave', handleDragLeave, false);
        col.addEventListener('drop', handleDrop, false);
        col.addEventListener('dragend', handleDragEnd, false);
        col.style.cursor = "move";
    });
}

function makeEditable() {
    addRemove();
    addCallbacks();

    var ed = document.getElementById("editing");
    ed.innerHTML = "<p style=\"color:red\">You can edit by deleting the entry with the small red x next to row, adding to the directions or ingredients list, or reorder the direction rows by drag and dropping</p>";

    addIngredientForm();
    addDirectionForm();
    addCourseForm();
    addCountryForm();

    var eb = document.getElementById("editbutton");
    eb.disabled = true;

    var sb = document.getElementById("savebutton");
    sb.disabled = false;

}

function deleterecipe() {

    if (confirm('Are you sure you want to delete this recipe?')) {
        var o = new Object()
        o.id = recipeId;
        var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
        xmlhttp.open("POST", "/deleterecipe");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.send(JSON.stringify(o));
        window.location.replace("listrecipes");

    }

}

function saveAll() {


    var dirnum = 1;
    var dirlist = [];

    var table = document.getElementById('directions');

    rows = table.rows;
    for (var i = 0; i < rows.length; i++) {
        var dirobj = new Object();
        dirobj.direction = rows[i].cells[1].innerHTML;
        dirlist = dirlist.concat(dirobj);
    }


    var ingnum = 1;
    var ingrlist = [];
    table = document.getElementById('ingredients');

    rows = table.rows;
    for (var i = 0; i < rows.length; i++) {

        var ingobj = new Object();
        ingobj.ingredient = rows[i].cells[0].innerHTML;
        ingobj.amount = rows[i].cells[1].innerHTML;
        ingobj.allergen = rows[i].cells[2].innerHTML;
        ingrlist = ingrlist.concat(ingobj);

    }
    var ingrObj = new Object();

    ingrObj.name = recipeName;
    ingrObj.country = document.getElementById("country").value;
    ingrObj.course = document.getElementById("course").value;
    ingrObj.author = recipeAuthor;
    ingrObj.views = recipeViews;
    ingrObj.id = recipeId;
    ingrObj.image = recipeImage;
    ingrObj.ingredients = ingrlist;
    ingrObj.directions = dirlist;
    var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
    xmlhttp.open("POST", "/updaterecipe");
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.send(JSON.stringify(ingrObj));



    var eb = document.getElementById("editbutton");
    eb.disabled = false;

    var sb = document.getElementById("savebutton");
    sb.disabled = true;

    removeRemove();
    var iform = document.getElementById("ingredientform");
    iform.innerHTML = "";
    iform = document.getElementById("directionform");
    iform.innerHTML = "";
    iform = document.getElementById("courseform");
    iform.innerHTML = "";
    iform = document.getElementById("countryform");
    iform.innerHTML = "";
    var ed = document.getElementById("editing");
    ed.innerHTML = "";

    window.location.href = "/listrecipes";

}