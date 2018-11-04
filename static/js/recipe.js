
// Adds ingredient to table
function addIngredient() {
    // Remove the 'remove item' 'X' after each element in table
    removeRemove();

    // Get data to add ingredient
    var id = document.getElementById("ingredient");
    var aid = document.getElementById("allergen");
    var tid = document.getElementById("ingredients");
    var amid = document.getElementById("amount");

    // Add the ingredient data to table from form
    tid.innerHTML += "<tr><td class=\"myfont table-padding\">" + id.value + "</td><td class=\"myfont table-padding\">" + amid.value + "</td><td class=\"myfont table-padding\">" + aid.value + "</td></tr>";
    // Reset form items to empty
    id.value = '';
    aid.value = '';
    amid.value = '';

    // Add the 'remove item' 'X' after each element in the table so they can continue to remove items
    addRemove();
}

// Add direction to table
function addDirection() {
    // Remove the 'remove item' 'X' after each element in table
    removeRemove();
    // Get the data to add directions and the table itself
    var id = document.getElementById("direction");
    var tid = document.getElementById("directions");

    // Get row length as current direction number to place into  table
    var rows = tid.rows;
    var dirnum = tid.rows.length;
    
    // Insert the direction into table
    tid.innerHTML += "<tr draggable=\"true\" class=\"column\" style=\"cursor: move;\"><td class=\"myfont table-padding\">" + dirnum++ + "</td><td class=\"myfont table-padding\">" + id.value + "</td></tr>";

    // Reset value
    id.value = '';
    // Add the callbacks for the drop-and-drag table so user can reposition the recipe directions
    addCallbacks();

    // Add the 'remove item' 'X' after each element in the table so they can continue to remove items
    addRemove();
}

// The source element from where the dragging happens
var dragSrcEl = null;

// This function reorders the direction positions in the recipe directions table
function reorder() {
    var table = document.getElementById('directions');

    rows = table.rows;
    for (var i = 0; i < rows.length; i++) {
        rows[i].cells[0].innerHTML = i;
    }
}

// Handle Drag Over event
function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }

    // Effect of the drag over event on the table
    e.dataTransfer.dropEffect = 'move';

    return false;
}

// Handle Drag Ender event
function handleDragEnter(e) {
    this.classList.add('over');

}

// Handle Drag Over event
function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }

    // Give the move drop Effect
    e.dataTransfer.dropEffect = 'move';

    return false;

}

// Handle Drag Leave event
function handleDragLeave(e) {
    this.classList.remove('over');

}

// Handle Drag End event (Release button )
function handleDragEnd(e) {
    var cols = document.querySelectorAll('#directions .column');
    [].forEach.call(cols, function (col) {
        col.classList.remove('over');
    });

    // Reorder after drag end
    reorder();
}

// Handle the drop
function handleDrop(e) {

    if (e.stopPropagation) {
        e.stopPropagation(); // Stops some browsers from redirecting.
    }
    if (dragSrcEl != this) {
        dragSrcEl.innerHTML = this.innerHTML;
        this.innerHTML = e.dataTransfer.getData('text/html');
    }
    // Remove the 'remove X' items on the tables
    removeRemove();
    // Add the 'remove X' items on the tables.
    // This is done to refresh the 'X' on the tables when something is moved
    addRemove();

    return false;
}

// Handle Drag Start event
function handleDragStart(e) {
    dragSrcEl = this;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}


// Remove the 'X items' on the recipe directions table
// and ingredients table 
function removeRemove() {

    var table = document.getElementById('directions');

    rows = table.rows;
    // Iterate over the table rows and delete last cell
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
    // Iterate over the table rows and delete last cell
    for (var i = 0; i < rows.length; i++) {
        for (var j = 0; j < rows[i].cells.length; j++) {
            if (rows[i].cells[j].innerHTML == 'x') {
                table.rows[i].deleteCell(j);
                break;
            }
        }
    }

}

// Add the remove 'X items' on the directions and ingredients tables
function addRemove() {

    var table = document.getElementById('directions');
    var rows = table.rows;
    // Iterate over the rows and insert a red 'x' in the last cell
    for (var i = 0; i < rows.length; i++) {

        cell = rows[i].insertCell(rows[i].cells.length);
        cell.style.color = "red";
        cell.innerHTML = "x";

        // Create a mouseover pointer on the X when the user hovers
        // over the small X, and add a callback to the onclick event
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
            // Reorder directions table
            reorder();

        }, false);
    }

    var table = document.getElementById('ingredients');
    var rows = table.rows;
    // Iterate over the rows and add a small 'X' to indicate to the user they can delete
    // the item in the row. Add to last cell.
    for (var i = 1; i < rows.length; i++) {

        cell = rows[i].insertCell(rows[i].cells.length);
        cell.style.color = "red";
        cell.innerHTML = "x";


        // Create a mouseover pointer on the X when the user hovers
        // over the small X, and add a callback to the onclick event 
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

// This function adds the direction form to the table when 
// the user hits the edit button
function addDirectionForm() {
    var iform = document.getElementById("directionform");
    // Create a form
    f = document.createElement("form");
    // Action
    f.setAttribute("action", "javascript:addDirection()");
    f.setAttribute("method", "POST");

    // Input data
    i1 = document.createElement("input");
    i1.type = "text";
    i1.id = "direction";
    i1.setAttribute('size', 50);
    i1.placeholder = "Direction";
    f.appendChild(i1);

    // Button
    i4 = document.createElement("input");
    i4.type = "submit";
    i4.className = "btn btn-primary myfont";
    i4.value = "Add Direction";
    f.appendChild(i4);


    iform.appendChild(f);
}

// This function adds the course form to the table when 
// the user hits the edit button
function addCourseForm() {
    // Form created
    var iform = document.getElementById("courseform");
    f = document.createElement("form");
    // Action
    f.setAttribute("action", "");
    f.setAttribute("method", "POST");

    // Input
    i1 = document.createElement("input");
    i1.type = "text";
    i1.id = "course"
    i1.value = recipeCourse;
    f.appendChild(i1);

    iform.appendChild(f);
}

// This function adds the country form to the table when 
// the user hits the edit button
function addCountryForm() {
    var iform = document.getElementById("countryform");
    // Create form
    f = document.createElement("form");
    // ACTION
    f.setAttribute("action", "");
    f.setAttribute("method", "POST");

    // INPUT element
    i1 = document.createElement("input");
    i1.type = "text";
    i1.id = "country"
    i1.value = recipeCountry;
    f.appendChild(i1);

    iform.appendChild(f);
}

// This function adds the ingredient form to the table when 
// the user hits the edit button

function addIngredientForm() {
    var iform = document.getElementById("ingredientform");
    // Form
    f = document.createElement("form");
    // Action calls addIngredient() function in javascript
    f.setAttribute("action", "javascript:addIngredient()");
    f.setAttribute("method", "POST");

    // Input element
    i1 = document.createElement("input");
    i1.type = "text";
    i1.id = "ingredient";
    i1.placeholder = "Ingredient";
    f.appendChild(i1);

    i2 = document.createElement("input");
    i2.type = "text";
    i2.id = "amount";
    i2.setAttribute('size', 10);
    i2.placeholder = "Amount";
    f.appendChild(i2);

    i3 = document.createElement("input");
    i3.type = "text";
    i3.id = "allergen";
    i3.setAttribute('size', 10);
    i3.placeholder = "Allergen";
    f.appendChild(i3);

    i4 = document.createElement("input");
    i4.type = "submit";
    i4.className = "btn btn-primary myfont";
    i4.value = "Add Ingredient";
    f.appendChild(i4);


    iform.appendChild(f);
}

// Add callbacks to directions table to make the drag and drop functionality
// of the table work.
function addCallbacks() {
    var cols = document.querySelectorAll('#directions .column');
    [].forEach.call(cols, function (col) {

        // All events handled in included file above
        col.addEventListener('dragstart', handleDragStart, false);
        col.addEventListener('dragenter', handleDragEnter, false);
        col.addEventListener('dragover', handleDragOver, false);
        col.addEventListener('dragleave', handleDragLeave, false);
        col.addEventListener('drop', handleDrop, false);
        col.addEventListener('dragend', handleDragEnd, false);
        col.style.cursor = "move";
    });
}

// This function makes the recipe editable
function makeEditable() {
    // Add the remove item 'X' to the recipe tables
    addRemove();
    // Add callbacks to the drag and drop table
    addCallbacks();

    // Add some guidance for the user
    var ed = document.getElementById("editing");
    ed.innerHTML = "<p style=\"color:red\">You can edit by deleting the entry with the small red x next to row, adding to the directions or ingredients list, or reorder the direction rows by drag and dropping</p>";

    // Add the forms that can be edited
    addIngredientForm();
    addDirectionForm();
    addCourseForm();
    addCountryForm();

    // Set buttons enable / disabled
    var eb = document.getElementById("editbutton");
    eb.disabled = true;

    var sb = document.getElementById("savebutton");
    sb.disabled = false;

}

// This function is called when the user hits delete recipe
// It send an AJAX request to backend to delete the recipe
function deleterecipe() {

    // Confirm first before deleting a recipe
    if (confirm('Are you sure you want to delete this recipe?')) {
        // Create object to serialise to JSON
        var o = new Object()
        o.id = recipeId;
        // New AJAX POST
        var xmlhttp = new XMLHttpRequest(); 
        xmlhttp.open("POST", "/deleterecipe");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        // Serialise
        xmlhttp.send(JSON.stringify(o));
        // Redirect back to recipe list so recipe is deleted in list
        window.location.href = "/listrecipes";
    }
}

// Save the edited recipe
// This function is called when the Save button is hit
function saveAll() {
    // directory position
    var dirnum = 1;
    // object list collection
    var dirlist = [];

    var table = document.getElementById('directions');

    // Iterate over table and append directions to list
    rows = table.rows;
    for (var i = 0; i < rows.length; i++) {
        var dirobj = new Object();
        dirobj.direction = rows[i].cells[1].innerHTML;
        dirlist = dirlist.concat(dirobj);
    }


    var ingnum = 1;
    var ingrlist = [];
    table = document.getElementById('ingredients');

    // Iterate over ingredients table and append individual ingredients
    // to list
    rows = table.rows;
    for (var i = 1; i < rows.length; i++) {

        var ingobj = new Object();
        ingobj.ingredient = rows[i].cells[0].innerHTML;
        ingobj.amount = rows[i].cells[1].innerHTML;
        ingobj.allergen = rows[i].cells[2].innerHTML;
        ingrlist = ingrlist.concat(ingobj);

    }

    // Create an object to serialise to JSON
    var ingrObj = new Object();

    // All the data retrieved from the forms --
    // add all data to the object
    ingrObj.name = recipeName;
    ingrObj.country = document.getElementById("country").value;
    ingrObj.course = document.getElementById("course").value;
    ingrObj.author = recipeAuthor;
    ingrObj.views = recipeViews;
    ingrObj.id = recipeId;
    ingrObj.image = recipeImage;
    // Collections
    ingrObj.ingredients = ingrlist;
    ingrObj.directions = dirlist;
    // New AJAX POST
    var xmlhttp = new XMLHttpRequest();  
    // Send to this backend address
    xmlhttp.open("POST", "/updaterecipe");
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    // Serialise 
    xmlhttp.send(JSON.stringify(ingrObj));


    // Enable / Disable buttons again once saved

    var eb = document.getElementById("editbutton");
    eb.disabled = false;

    var sb = document.getElementById("savebutton");
    sb.disabled = true;

    // Remove the 'remove X items' on tables
    removeRemove();

    // Reset data
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

    // Redirect back to list
    window.location.href = "/listrecipes";

}