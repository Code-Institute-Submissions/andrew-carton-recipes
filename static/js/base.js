$('#registerModal').on('show.bs.modal', function (event) { })

function onRegisterSubmit() {
    username = document.getElementById("username");
    password = document.getElementById("password");
    

    var xmlhttp = new XMLHttpRequest(); 
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert("Creation succeeded! Login now!");
            $('#registerModal').modal('hide');
        }
        else if (this.readyState == 4 && this.status == 500) {
            var data = JSON.parse(this.responseText);
            alert(data['message']);
        }
    }
    var authObj = new Object();
    authObj.username = username.value;
    authObj.password = password.value;
    xmlhttp.open("POST", "/register", true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    
    xmlhttp.send(JSON.stringify(authObj));
}