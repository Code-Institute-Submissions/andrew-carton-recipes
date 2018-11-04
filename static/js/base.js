// Register the two Register and Login modals with jquery
$('#registerModal').on('show.bs.modal', function (event) { })
$('#loginModal').on('show.bs.modal', function (event) { })

// Function when registration is submitted
// Creates AJAX request and waits for return

function onRegisterSubmit() {
    // Get the username and password from the DOM
    username = document.getElementById("username");
    password = document.getElementById("password");


    // Create an AJAX request
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        // AJAX on ready function

        // If success (response 200)
        if (this.readyState == 4 && this.status == 200) {
            alert("Creation succeeded! Login now!");
            $('#registerModal').modal('hide');
        }
        // If failure (response 500)
        else if (this.readyState == 4 && this.status == 500) {
            var data = JSON.parse(this.responseText);
            alert(data['message']);
        }
    }
    // Create an object to serialise json
    var authObj = new Object();
    authObj.username = username.value;
    authObj.password = password.value;
    // Open and set Request header of AJAX request to JSON
    xmlhttp.open("POST", "/register", true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");

    // Send JSON
    xmlhttp.send(JSON.stringify(authObj));
}

// Function that is called when Login is submitted
// Creates an AJAX request and processes callback return

function onLoginSubmit() {
    
    // Get username and password of login from DOM
    username = document.getElementById("username1");
    password = document.getElementById("password1");

    // New AJAX request
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        // On success (200)
        if (this.readyState == 4 && this.status == 200) {
            alert("Login Successful");
            $('#loginModal').modal('hide');
            window.location.replace("/");
        }
        // On Failure (500)
        else if (this.readyState == 4 && this.status == 500) {
            var data = JSON.parse(this.responseText);
            alert(data['message']);
        }
    }
    // Create an object for serialisations of json
    var authObj = new Object();
    authObj.username = username.value;
    authObj.password = password.value;
    // Set AJAX properties
    xmlhttp.open("POST", "/login", true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");

    // Serialise and send JSON
    xmlhttp.send(JSON.stringify(authObj));
}
